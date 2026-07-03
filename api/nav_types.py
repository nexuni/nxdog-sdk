"""
nav_types
=========

Platform-independent data types for the nxnav navigation stack.

These types have NO ROS dependency and can be used by any Python application
to interact with nxnav.
"""

from dataclasses import dataclass, field
from enum import IntEnum
from typing import List


class NavResultCode(IntEnum):
    """Result codes for navigation operations.

    These match the status codes used internally by the navigator nodes.
    """
    SUCCESS = 0
    LOCALIZATION_FAIL = 1
    CANCELLED = 2
    STUCK = 3
    PLANNING_FAIL = 4


@dataclass
class Pose2D:
    """2D pose on a map.

    Attributes:
        x: X position in meters (map frame).
        y: Y position in meters (map frame).
        yaw: Heading in radians (counter-clockwise from +X axis).
    """
    x: float = 0.0
    y: float = 0.0
    yaw: float = 0.0


@dataclass
class Pose3D:
    """Full 3D pose with quaternion orientation.

    Attributes:
        x, y, z: Position in meters (map frame).
        qx, qy, qz, qw: Quaternion orientation (ROS convention, w-last storage).
    """
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    qx: float = 0.0
    qy: float = 0.0
    qz: float = 0.0
    qw: float = 1.0


@dataclass
class NavGoal:
    """A navigation goal specifying where the robot should go.

    Attributes:
        map_name: Map group name (e.g., "floor6", "sb"). nxnav auto-resolves
                  to the correct tile based on position.
        x: Goal X position in meters (map frame).
        y: Goal Y position in meters (map frame).
        yaw: Goal heading in radians.
        goal_tolerance_xy: Position tolerance in meters (default from config).
        goal_tolerance_yaw: Heading tolerance in radians (default from config).
    """
    map_name: str
    x: float
    y: float
    yaw: float = 0.0
    goal_tolerance_xy: float = 0.3
    goal_tolerance_yaw: float = 0.1
    nav_speed: float = 0.65

@dataclass
class NavResult:
    """Result of a navigation operation.

    Attributes:
        success: True if the goal was reached within tolerance.
        status_code: Numeric result code (see NavResultCode).
        message: Human-readable description of the result.
    """
    success: bool
    status_code: int
    message: str = ""

    @property
    def code(self) -> NavResultCode:
        """Return the status_code as a NavResultCode enum."""
        try:
            return NavResultCode(self.status_code)
        except ValueError:
            return NavResultCode.PLANNING_FAIL


@dataclass
class NavPlan:
    """A planned navigation path.

    Attributes:
        path: List of [x, y] waypoints in map frame (meters).
        map_name: Name of the map this path is on.
    """
    path: List[List[float]] = field(default_factory=list)
    map_name: str = ""

    @property
    def is_empty(self) -> bool:
        return len(self.path) == 0


@dataclass
class Velocity:
    """2D velocity command.

    Attributes:
        vx: Linear velocity in X (forward) in m/s.
        vy: Linear velocity in Y (left) in m/s.
        wz: Angular velocity about Z (counter-clockwise) in rad/s.
    """
    vx: float = 0.0
    vy: float = 0.0
    wz: float = 0.0


@dataclass
class MapInfo:
    """Information about a loaded map.

    Attributes:
        name: Map name (e.g., "floor6_p0_p0").
        group: Map group (e.g., "floor6").
        resolution: Map resolution in meters/pixel.
        origin_x: World X coordinate of the map image origin.
        origin_y: World Y coordinate of the map image origin.
        width: Map width in pixels.
        height: Map height in pixels.
    """
    name: str = ""
    group: str = ""
    resolution: float = 0.1
    origin_x: float = 0.0
    origin_y: float = 0.0
    width: int = 0
    height: int = 0


@dataclass
class Zone:
    """A zone on a map with special navigation behavior.

    Attributes:
        name: Zone identifier.
        type: Zone type - "door", "stair", "elevator", "config", "map".
        polygon: List of [x, y] vertices defining the zone boundary.
    """
    name: str
    type: str
    polygon: List[List[float]] = field(default_factory=list)


@dataclass
class Portal:
    """A connection between two maps in the map graph.

    Attributes:
        name: Portal identifier.
        type: Portal type - "level", "stair-up", "stair-down", "elevator".
        src_map: Source map name.
        dst_map: Destination map name.
        cost: Traversal cost for graph routing.
    """
    name: str
    type: str
    src_map: str
    dst_map: str
    cost: float = 1.0
