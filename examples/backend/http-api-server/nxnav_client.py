"""
nxnav_client.nxnav_client
==========================

Platform-independent Python API for controlling the nxnav navigation stack.

This module provides ``NxNavClient``, the primary interface that Python
applications use to command navigation.  The public API surface has
**no ROS dependency** — all arguments and return values are plain Python types
or dataclasses from :mod:`nav_types`.

Internally, the client spins an ``rclpy`` node in a daemon thread to
communicate with the nxnav ROS 2 nodes.  This follows the same pattern as
nav2's ``BasicNavigator`` from ``nav2_simple_commander``.

Usage::

    from nxnav_client import NxNavClient, NavGoal

    nav = NxNavClient(config_path="/path/to/nxnav_params.yaml")
    nav.start()

    # Navigate to a goal
    nav.goto(NavGoal(map_name="floor6", x=5.0, y=3.0, yaw=1.57))

    # Check pose
    pose = nav.get_pose()

    nav.stop()
"""

from __future__ import annotations

import math
import threading
import time
from typing import Callable, Optional

from nav_types import (
    NavGoal,
    NavPlan,
    NavResult,
    Pose2D,
    Velocity,
)

HEARTBEAT_TIMEOUT_SEC = 6.0
CURRENT_MAP_TIMEOUT_SEC = 3.0

# ---------------------------------------------------------------------------
# Type aliases for callbacks
# ---------------------------------------------------------------------------
ResultCallback = Optional[Callable[[NavResult], None]]
MapCallback = Optional[Callable[[bool], None]]


class NxNavClient:
    """High-level navigation client.

    This is the main class application code needs to import.
    It owns the internal ROS 2 node while exposing only plain Python
    dataclasses and values to callers.

    Parameters
    ----------
    config_path : str, optional
        Absolute path to ``nxnav_params.yaml``.  When provided, map
        directories, default tolerances, and localization topic names are
        read from this file.  When omitted, built-in defaults are used.
    """

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def __init__(self, config_path: str | None = None):
        self._config_path = config_path
        self._started = False
        self._state_lock = threading.Lock()

        # State (updated by internal ROS subscriptions)
        self._pose: Pose2D = Pose2D()
        self._velocity: Velocity = Velocity()
        self._current_map: str | None = None
        self._last_map_update_time: float | None = None
        self._current_plan: NavPlan = NavPlan()
        self._current_goal: NavGoal | None = None
        self._last_heartbeat_time: float | None = None

        # ROS internals — initialised in start()
        self._node = None
        self._executor = None
        self._spin_thread: threading.Thread | None = None
        self._nav_goal_handle = None
        self._result_callback = None
        self._cmd_vel_pubs = {}
        self._avoidance_pub = None
        self._initial_pose_pub = None
        self._nav_action = None
        self._compute_prm_path_action = None
        self._switch_map_client = None
        self._set_map_client = None

    def start(self) -> None:
        """Initialise the internal ROS 2 node and begin spinning.

        Must be called once before any other method.  Safe to call from
        any thread.  The ROS executor runs in a background daemon thread
        so it does not block the caller.

        Raises
        ------
        RuntimeError
            If ``rclpy`` is not installed or ROS 2 is not available.
        """
        if self._started:
            return

        import rclpy
        from rclpy.executors import MultiThreadedExecutor

        if not rclpy.ok():
            rclpy.init()

        self._create_ros_node()
        self._executor = MultiThreadedExecutor()
        self._executor.add_node(self._node)

        self._spin_thread = threading.Thread(
            target=self._executor.spin, daemon=True
        )
        self._spin_thread.start()
        self._started = True

    def stop(self) -> None:
        """Shut down the internal ROS 2 node and executor.

        After calling ``stop()``, this client instance must not be reused.
        """
        if not self._started:
            return
        self._executor.shutdown()
        if self._spin_thread is not None:
            self._spin_thread.join(timeout=2.0)
        # Destroy action clients before the node to avoid InvalidHandle.
        for action_client in (
            self._nav_action,
            self._compute_prm_path_action,
        ):
            if action_client is not None:
                action_client.destroy()
        if self._node is not None:
            self._node.destroy_node()
        self._started = False

    def is_ready(self) -> bool:
        """Return True when the client is initialized enough to accept calls."""
        return (
            self._started
            and self._node is not None
            and self._executor is not None
            and self._spin_thread is not None
            and self._spin_thread.is_alive()
            and self._nav_action is not None
            and self._compute_prm_path_action is not None
            and self._switch_map_client is not None
            and self._set_map_client is not None
        )

    # ------------------------------------------------------------------
    # Status queries
    # ------------------------------------------------------------------

    def get_pose(self) -> Pose2D:
        """Return the current robot pose in the map frame."""
        self._ensure_started()
        with self._state_lock:
            return Pose2D(
                x=self._pose.x, y=self._pose.y, yaw=self._pose.yaw
            )

    def get_plan(self) -> NavPlan:
        """Return the current active navigation plan."""
        self._ensure_started()
        with self._state_lock:
            return NavPlan(
                path=list(self._current_plan.path),
                map_name=self._current_plan.map_name,
            )

    def get_velocity(self) -> Velocity:
        """Return the current filtered velocity."""
        self._ensure_started()
        with self._state_lock:
            return Velocity(
                vx=self._velocity.vx,
                vy=self._velocity.vy,
                wz=self._velocity.wz,
            )

    def get_current_map(self) -> str | None:
        """Return the name of the currently active map."""
        self._ensure_started()
        with self._state_lock:
            if (
                self._current_map is not None
                and self._last_map_update_time is not None
                and (time.monotonic() - self._last_map_update_time)
                > CURRENT_MAP_TIMEOUT_SEC
            ):
                self._current_map = None
                self._last_map_update_time = None
            return self._current_map

    def get_current_goal(self) -> NavGoal | None:
        """Return the active navigation goal, if one is in progress."""
        self._ensure_started()
        with self._state_lock:
            if self._current_goal is None:
                return None
            return NavGoal(
                map_name=self._current_goal.map_name,
                x=self._current_goal.x,
                y=self._current_goal.y,
                yaw=self._current_goal.yaw,
                goal_tolerance_xy=self._current_goal.goal_tolerance_xy,
                goal_tolerance_yaw=self._current_goal.goal_tolerance_yaw,
                nav_speed=self._current_goal.nav_speed,
            )

    def is_alive(self) -> bool:
        """Return True when heartbeat messages are arriving recently enough."""
        self._ensure_started()
        with self._state_lock:
            last_heartbeat_time = self._last_heartbeat_time

        if last_heartbeat_time is None:
            return False

        return (time.monotonic() - last_heartbeat_time) <= HEARTBEAT_TIMEOUT_SEC

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_started(self) -> None:
        if not self._started:
            raise RuntimeError(
                "NxNavClient.start() must be called before using the client."
            )

    def _update_pose(self, x: float, y: float, yaw: float) -> None:
        with self._state_lock:
            self._pose = Pose2D(x=x, y=y, yaw=yaw)

    def _update_velocity(self, vx: float, vy: float, wz: float) -> None:
        with self._state_lock:
            self._velocity = Velocity(vx=vx, vy=vy, wz=wz)

    def _update_current_map(self, map_name: str | None) -> None:
        with self._state_lock:
            self._current_map = map_name
            self._last_map_update_time = time.monotonic()

    def _update_current_goal(self, goal: NavGoal | None) -> None:
        with self._state_lock:
            self._current_goal = goal

    def _mark_heartbeat_received(self) -> None:
        with self._state_lock:
            self._last_heartbeat_time = time.monotonic()

    def _create_ros_node(self) -> None:
        from rclpy.node import Node
        from rclpy.qos import QoSDurabilityPolicy, QoSProfile

        class _Inner(Node):
            pass

        self._node = _Inner('nxnav_client_node')

        # -- Lazy imports of ROS msg types -----------
        from geometry_msgs.msg import PoseWithCovarianceStamped, Twist
        from nav_msgs.msg import Odometry
        from std_msgs.msg import Bool, String

        from nxnav_msgs.action import ComputePrmPath as ComputePrmPathAction
        from nxnav_msgs.action import NavigateToPose
        from nxnav_msgs.srv import SwitchMap

        from rclpy.action import ActionClient

        latched = QoSProfile(
            depth=1, durability=QoSDurabilityPolicy.TRANSIENT_LOCAL)

        # -- Subscriptions --
        self._node.create_subscription(
            Odometry, '/nxnav/odom', self._odom_cb, 10)
        self._node.create_subscription(
            String, '/nxnav/current_map', self._map_cb, latched)
        self._node.create_subscription(
            Bool, '/nxnav/heartbeat', self._heartbeat_cb, 10)

        # -- Publishers --
        self._cmd_vel_pubs = {
            'low': self._node.create_publisher(Twist, '/cmd_vel_low', 10),
            'mid': self._node.create_publisher(Twist, '/cmd_vel_mid', 10),
            'high': self._node.create_publisher(Twist, '/cmd_vel_high', 10),
        }
        self._avoidance_pub = self._node.create_publisher(
            Bool, '/nxnav/avoidance_enabled', latched)
        self._initial_pose_pub = self._node.create_publisher(
            PoseWithCovarianceStamped, '/initialpose', 10)

        # -- Action clients --
        self._nav_action = ActionClient(
            self._node, NavigateToPose, '/nxnav/navigate_to_pose')
        self._compute_prm_path_action = ActionClient(
            self._node, ComputePrmPathAction, '/nxnav/compute_prm_path')

        # -- Service clients --
        self._switch_map_client = self._node.create_client(
            SwitchMap, '/nxnav/switch_map')
        self._set_map_client = self._node.create_client(
            SwitchMap, '/nxnav/set_map')

    # -- Subscription callbacks --

    def _odom_cb(self, msg):
        p = msg.pose.pose
        yaw = math.atan2(
            2.0 * (p.orientation.w * p.orientation.z +
                   p.orientation.x * p.orientation.y),
            1.0 - 2.0 * (p.orientation.y ** 2 + p.orientation.z ** 2))
        self._update_pose(p.position.x, p.position.y, yaw)

        t = msg.twist.twist
        self._update_velocity(t.linear.x, t.linear.y, t.angular.z)

    def _map_cb(self, msg):
        self._update_current_map(msg.data or None)

    def _heartbeat_cb(self, msg):
        del msg
        self._mark_heartbeat_received()

    # -- Navigation --

    def goto(
        self,
        goal: NavGoal,
        result_callback: ResultCallback = None,
    ) -> None:
        """Send NavigateToPose action goal."""
        self._ensure_started()
        from nxnav_msgs.action import NavigateToPose

        self._result_callback = result_callback
        self._update_current_goal(goal)

        if not self._nav_action.wait_for_server(timeout_sec=5.0):
            self._update_current_goal(None)
            if result_callback:
                result_callback(NavResult(
                    success=False, status_code=4,
                    message='NavigateToPose action server not available'))
            return

        goal_msg = NavigateToPose.Goal()
        goal_msg.goal.header.frame_id = 'map'
        goal_msg.goal.pose.position.x = float(goal.x)
        goal_msg.goal.pose.position.y = float(goal.y)
        goal_msg.goal.pose.orientation.z = math.sin(goal.yaw / 2.0)
        goal_msg.goal.pose.orientation.w = math.cos(goal.yaw / 2.0)
        goal_msg.goal_map = goal.map_name
        goal_msg.goal_tolerance_xy = float(goal.goal_tolerance_xy)
        goal_msg.goal_tolerance_yaw = float(goal.goal_tolerance_yaw)
        goal_msg.nav_speed = float(goal.nav_speed)

        future = self._nav_action.send_goal_async(
            goal_msg, feedback_callback=self._nav_feedback_cb)
        future.add_done_callback(self._nav_goal_response_cb)

    def _nav_goal_response_cb(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self._update_current_goal(None)
            if self._result_callback:
                self._result_callback(NavResult(
                    success=False, status_code=4,
                    message='Goal rejected'))
            return
        self._nav_goal_handle = goal_handle
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._nav_result_cb)

    def _nav_result_cb(self, future):
        result = future.result().result
        success = result.error_code == 0

        self._node.get_logger().info(
            f'[_nav_result_cb] code: {result.error_code}, msg: {result.error_msg}')

        nav_result = NavResult(
            success=success,
            status_code=result.error_code,
            message=result.error_msg,
        )
        self._update_current_goal(None)
        if self._result_callback:
            self._result_callback(nav_result)

    def _nav_feedback_cb(self, feedback_msg):
        del feedback_msg

    def plan(self, start_map=None, start=None, goal_map=None, goal=None):
        """Compute a visualization path through the PRM graph."""
        self._ensure_started()
        from nxnav_msgs.action import ComputePrmPath as ComputePrmPathAction

        if start_map is None or start is None or goal_map is None or goal is None:
            current_goal = self.get_current_goal()
            if current_goal is None:
                self._node.get_logger().info('[plan] no current goal')
                return NavPlan()
            pose = self.get_pose()
            if start_map is None:
                start_map = self.get_current_map()
            if start is None:
                start = [pose.x, pose.y]
            if goal_map is None:
                goal_map = current_goal.map_name
            if goal is None:
                goal = [current_goal.x, current_goal.y]

        if start_map is None:
            self._node.get_logger().info('[plan] missing start map')
            return NavPlan()

        if goal_map is None:
            goal_map = start_map
        if goal is None:
            self._node.get_logger().info('[plan] missing goal')
            return NavPlan()

        if not self._compute_prm_path_action.wait_for_server(timeout_sec=5.0):
            self._node.get_logger().info(
                '[plan] ComputePrmPath action server not available')
            return NavPlan()

        goal_msg = ComputePrmPathAction.Goal()
        goal_msg.start_map = start_map
        goal_msg.goal_map = goal_map
        goal_msg.smooth = True
        goal_msg.start.header.frame_id = 'map'
        goal_msg.start.pose.position.x = float(start[0])
        goal_msg.start.pose.position.y = float(start[1])
        goal_msg.start.pose.orientation.w = 1.0
        goal_msg.goal.header.frame_id = 'map'
        goal_msg.goal.pose.position.x = float(goal[0])
        goal_msg.goal.pose.position.y = float(goal[1])
        goal_msg.goal.pose.orientation.w = 1.0

        future = self._compute_prm_path_action.send_goal_async(goal_msg)
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            if future.done():
                break
            time.sleep(0.05)
        if not future.done():
            self._node.get_logger().info('[plan] PRM path goal not accepted')
            return NavPlan()

        goal_handle = future.result()
        if not goal_handle or not goal_handle.accepted:
            self._node.get_logger().info('[plan] PRM path goal rejected')
            return NavPlan()

        result_future = goal_handle.get_result_async()
        deadline = time.monotonic() + 60.0
        while time.monotonic() < deadline:
            if result_future.done():
                break
            time.sleep(0.05)
        if not result_future.done():
            self._node.get_logger().info('[plan] PRM path action timed out')
            return NavPlan()

        result = result_future.result().result
        if result.error_code != 0:
            self._node.get_logger().info(
                f'[plan] PRM path failed: {result.error_msg}')
            return NavPlan()

        path = [[ps.pose.position.x, ps.pose.position.y]
                for ps in result.path.poses]
        self._node.get_logger().info(f'[plan] PRM path points: {len(path)}')
        return NavPlan(path=path, map_name=goal_map)

    def compute_route(self, goals):
        """Compute one concatenated visualization route between ordered goals."""
        self._ensure_started()
        route = []
        for i in range(len(goals) - 1):
            plan = self.plan(
                goals[i].map_name,
                [goals[i].x, goals[i].y],
                goals[i + 1].map_name,
                [goals[i + 1].x, goals[i + 1].y],
            )
            if not plan.is_empty:
                if route and plan.path and route[-1] == plan.path[0]:
                    route.extend(plan.path[1:])
                else:
                    route.extend(plan.path)
        return route

    def pause(self):
        """Cancel the current NavigateToPose action and mark navigation paused."""
        self._ensure_started()
        if self._nav_goal_handle:
            self._nav_goal_handle.cancel_goal_async()

    def resume(self):
        """Resume navigation.

        Full resume requires re-sending the previous NavGoal.
        """
        self._ensure_started()

    def cancel(self):
        """Cancel all active goals."""
        self._ensure_started()
        if self._nav_goal_handle:
            self._nav_goal_handle.cancel_goal_async()
            self._nav_goal_handle = None
        self._update_current_goal(None)

    # -- Configuration --

    def set_tile(self, map_name, result_callback: MapCallback = None):
        """Call /nxnav/switch_map service."""
        self._ensure_started()
        from nxnav_msgs.srv import SwitchMap

        if not self._switch_map_client.wait_for_service(timeout_sec=5.0):
            if result_callback:
                result_callback(False)
            return

        self._node.get_logger().info(f'[set_tile] map_name: {map_name}.')

        req = SwitchMap.Request()
        req.map_name = map_name
        future = self._switch_map_client.call_async(req)
        future.add_done_callback(
            lambda f: self._set_tile_done(f, result_callback))

    def _set_tile_done(self, future, callback):
        result = future.result()
        success = result is not None and result.success
        self._node.get_logger().info(f'[_set_tile_done] success: {success}, msg: {result.message}.')
        if callback:
            callback(success)

    def set_map(self, map_name, result_callback: MapCallback = None):
        """Call /nxnav/set_map service to load a map group by name."""
        self._ensure_started()
        from nxnav_msgs.srv import SwitchMap

        if not self._set_map_client.wait_for_service(timeout_sec=5.0):
            if result_callback:
                result_callback(False)
            return

        self._node.get_logger().info(
            f'[set_map] map_name: {map_name}.')

        req = SwitchMap.Request()
        req.map_name = map_name
        req.load_3d = False
        future = self._set_map_client.call_async(req)
        future.add_done_callback(
            lambda f: self._set_map_done(f, result_callback))

    def _set_map_done(self, future, callback):
        result = future.result()
        success = result is not None and result.success
        message = result.message if result is not None else ''
        self._node.get_logger().info(
            f'[_set_map_done] success: {success}, msg: {message}.')
        if callback:
            callback(success)

    def set_initialpose(self, x, y, yaw, map_tile_name=None, callback=None):
        """Publish PoseWithCovarianceStamped to /initialpose."""
        self._ensure_started()
        if map_tile_name is None:
            self._node.get_logger().error('[set_initialpose] must provide map name.')
            return

        self._node.get_logger().info(f'[set_initialpose] x, y, yaw: {x}, {y}, {yaw}')

        if map_tile_name != self.get_current_map():
            self.set_tile(map_tile_name, lambda ok: self._do_set_initialpose(
                x, y, yaw, callback) if ok else (callback(False) if callback else None))
        else:
            self._do_set_initialpose(x, y, yaw, callback)

    def _do_set_initialpose(self, x, y, yaw, callback):
        from geometry_msgs.msg import PoseWithCovarianceStamped
        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = self._node.get_clock().now().to_msg()
        msg.pose.pose.position.x = float(x)
        msg.pose.pose.position.y = float(y)
        msg.pose.pose.orientation.z = math.sin(yaw / 2.0)
        msg.pose.pose.orientation.w = math.cos(yaw / 2.0)
        msg.pose.covariance[0] = 0.25
        msg.pose.covariance[7] = 0.25
        msg.pose.covariance[35] = 0.06
        self._initial_pose_pub.publish(msg)
        if callback:
            callback(True)

    def enable_avoidance(self, enabled):
        """Publish enable/disable to /nxnav/avoidance_enabled."""
        self._ensure_started()
        from std_msgs.msg import Bool
        msg = Bool()
        msg.data = enabled
        self._avoidance_pub.publish(msg)

    # -- Teleop --

    def set_cmd_vel(self, vx, vy, wz, priority):
        """Publish Twist to the appropriate /cmd_vel_* topic."""
        self._ensure_started()
        from geometry_msgs.msg import Twist
        msg = Twist()
        msg.linear.x = float(vx)
        msg.linear.y = float(vy)
        msg.angular.z = float(wz)
        pub = self._cmd_vel_pubs.get(priority, self._cmd_vel_pubs['low'])
        pub.publish(msg)
