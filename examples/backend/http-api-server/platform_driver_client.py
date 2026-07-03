import threading


class NxDogPlatformClient:
    """Platform-specific API for the Nxdog hardware layer."""

    def __init__(self):
        self.node = None
        self.executor = None
        self.spin_thread = None
        self.started = False

        self._is_ready = False
        self._is_charging = False
        self._auto_charging_callback = None

        self.vui_current_color = "blue"
        self.vui_current_brightness = 10

        self._String = None
        self._Twist = None
        self._Vector3 = None
        self._SportCommand = None

    def start(self):
        if self.started:
            return

        import rclpy
        from rclpy.executors import MultiThreadedExecutor
        from rclpy.node import Node
        from geometry_msgs.msg import Twist, Vector3
        from std_msgs.msg import String
        from sensor_msgs.msg import BatteryState
        from nxdog_interfaces.srv import SportCommand

        if not rclpy.ok():
            rclpy.init()

        self._String = String
        self._Twist = Twist
        self._Vector3 = Vector3
        self._SportCommand = SportCommand

        self.node = Node("nxdog_platform_client_node")
        self.executor = MultiThreadedExecutor()
        self.executor.add_node(self.node)
        self.spin_thread = threading.Thread(target=self.executor.spin, daemon=True)
        self.spin_thread.start()

        self.sport_client = self.node.create_client(SportCommand, "/nxdog/sport")

        self.pub_cmd_vui = self.node.create_publisher(String, "/nxdog/cmd_vui", 10)
        self.sub_battery = self.node.create_subscription(
            BatteryState, "/nxdog/battery", self._battery_callback, 10
        )

        self.pub_auto_charging_cmd = self.node.create_publisher(
            String, "/nxdog/auto_charging_cmd", 10
        )
        self.sub_auto_charging_result = self.node.create_subscription(
            String,
            "/nxdog/auto_charging_result",
            self._handle_auto_charging_result,
            10,
        )

        self.pub_speaker = self.node.create_publisher(String, "/nxdog/speaker", 10)
        self.set_ready_timer = self.node.create_timer(3.0, self._set_ready_flag)

        self.started = True
        self.vui_set_color(self.vui_current_color)

    def stop(self):
        if not self.started:
            return
        if self.executor is not None:
            self.executor.shutdown()
        if self.node is not None:
            self.node.destroy_node()
        self.started = False

    def set_sport_action(self, action):
        self._ensure_started()
        valid_sport_actions = [
            "StandUp",
            "StandDown",
            "BalanceStand",
            "Stretch",
            "Hello",
            "RecoveryStand",
            "FreeWalk",
            "StaticWalk",
            "Run",
            "WalkStair",
        ]
        if action not in valid_sport_actions:
            return
        if action == "StandUp":
            action = "RecoveryStand"

        req = self._SportCommand.Request()
        req.identifier = action
        self.sport_client.wait_for_service(timeout_sec=1.0)
        future = self.sport_client.call_async(req)
        future.add_done_callback(self._log_sport_response)

    def speaker_play(self, wav_file_path):
        self._ensure_started()
        msg = self._String()
        msg.data = wav_file_path
        self.pub_speaker.publish(msg)

    def auto_charging_start(self, callback):
        self._ensure_started()
        self.node.get_logger().info("start charging...")
        self._auto_charging_callback = callback
        msg = self._String()
        msg.data = "start"
        self.pub_auto_charging_cmd.publish(msg)

    def auto_charging_stop(self, callback):
        self._ensure_started()
        self.node.get_logger().info("stop charging...")
        self._auto_charging_callback = callback
        msg = self._String()
        msg.data = "stop"
        self.pub_auto_charging_cmd.publish(msg)

    def is_charging(self):
        return self._is_charging

    def vui_set_volume(self, level):
        self._ensure_started()
        level = min(max(int(level), 0), 10)
        msg = self._String()
        msg.data = f"set_volume,{level}"
        self.pub_cmd_vui.publish(msg)

    def vui_set_brightness(self, brightness):
        self._ensure_started()
        brightness = min(max(int(brightness), 0), 10)
        msg = self._String()
        msg.data = f"set_brightness_level,{brightness}"
        self.pub_cmd_vui.publish(msg)
        self.vui_current_brightness = brightness
        self.vui_current_color = "white"

    def vui_get_brightness(self):
        return self.vui_current_brightness

    def vui_set_color(self, color):
        self._ensure_started()
        valid_colors = ["white", "red", "yellow", "blue", "green", "cyan", "purple"]
        if color not in valid_colors:
            return
        msg = self._String()
        msg.data = f"set_color,{color}"
        self.pub_cmd_vui.publish(msg)
        self.vui_current_color = color
        self.vui_current_brightness = 10

    def vui_get_color(self):
        return self.vui_current_color

    def get_ready_flag(self):
        return self._is_ready

    def _ensure_started(self):
        if not self.started:
            raise RuntimeError("NxDogPlatformClient.start() must be called first.")

    def _battery_callback(self, msg):
        self._is_charging = msg.current > 0

    def _handle_auto_charging_result(self, msg):
        if self._auto_charging_callback is None:
            return
        result = msg.data == "true"
        callback = self._auto_charging_callback
        self._auto_charging_callback = None
        callback(result)

    def _set_ready_flag(self):
        self._is_ready = True
        self.set_ready_timer.cancel()

    def _log_sport_response(self, future):
        try:
            result = future.result()
            self.node.get_logger().info(
                f"/nxdog/sport response: {result.success}, {result.message}"
            )
        except Exception as exc:
            self.node.get_logger().error(f"/nxdog/sport call failed: {exc}")
