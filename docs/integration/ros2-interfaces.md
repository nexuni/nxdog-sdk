# ROS 2 Interfaces

The ROS 2 packages under `interfaces/` define the message, service, and action
types accepted by the robot-side nxnav and platform driver APIs.

They include:

- `nxnav_msgs`: navigation-related messages, services, and actions.
- `nxdog_interfaces`: platform-specific service definitions accepted by the
  platform driver.

These interfaces are part of the public integration contract for this developer
kit. Customer applications that communicate through ROS 2 should build against
these definitions so their messages match the robot-side services.

Build them with:

```bash
source /opt/ros/foxy/setup.bash
colcon build --base-paths interfaces --symlink-install
source install/setup.bash
```

Inspect them with:

```bash
ros2 interface show nxnav_msgs/action/NavigateToPose
ros2 interface show nxdog_interfaces/srv/SportCommand
```
