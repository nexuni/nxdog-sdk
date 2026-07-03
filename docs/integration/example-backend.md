# Example Backend Integration

The code under `examples/backend/http-api-server/` is reference example code
for exposing robot navigation and platform controls through a local HTTP API.
It was extracted from internal robot-side services and trimmed to show common
customer integration patterns.

This example is not a fully validated installer or production SDK. Treat it as
a template that may need changes for your robot software version, ROS 2 domain,
deployment layout, and customer application.

## What the Example Shows

- How to wrap nxnav ROS 2 navigation workflows behind HTTP endpoints.
- How to expose selected platform controls, including VUI color/brightness,
  VUI volume, charging state/control, and sport actions.
- How to use plain JSON requests and responses for customer-facing application
  integrations.

## Expected Environment

At a high level, the example expects:

- Ubuntu with ROS 2 Foxy.
- Python 3.
- Flask and Flask-Cors.
- Generated ROS 2 interfaces from `interfaces/`.
- Access to the robot's nxnav and platform ROS 2 topics, services, and actions.
- A map directory compatible with the robot navigation stack.

## Reference Setup

The commands below are a starting point, not a fully validated installation
procedure.

```bash
cd /home/unitree
git clone https://github.com/nexuni/nxdog-developer-kit.git nxdog-developer-kit
cd /home/unitree/nxdog-developer-kit
source /opt/ros/foxy/setup.bash
```

Install likely system dependencies:

```bash
sudo apt update
sudo apt install -y \
  python3-colcon-common-extensions \
  python3-pip \
  python3-rosdep \
  ros-foxy-geometry-msgs \
  ros-foxy-nav-msgs \
  ros-foxy-sensor-msgs \
  ros-foxy-std-msgs \
  ros-foxy-rosidl-default-generators \
  ros-foxy-rosidl-default-runtime
```

Install likely Python dependencies:

```bash
python3 -m pip install --user Flask Flask-Cors
```

Build the ROS 2 interface packages:

```bash
sudo rosdep init 2>/dev/null || true
rosdep update
rosdep install --from-paths interfaces --ignore-src -r -y
colcon build --base-paths interfaces --symlink-install
```

Source the generated interfaces before running the example HTTP server:

```bash
source /opt/ros/foxy/setup.bash
source /home/unitree/nxdog-developer-kit/install/setup.bash
```

You can check that the generated interfaces are visible with:

```bash
ros2 interface show nxnav_msgs/action/NavigateToPose
ros2 interface show nxdog_interfaces/srv/SportCommand
```

## Run the Example HTTP Server

The Flask server listens on port `5088`.

```bash
cd /home/unitree/nxdog-developer-kit
source /opt/ros/foxy/setup.bash
source install/setup.bash
export NXNAV_MAPS_DIR=/var/lib/nxdog/nxnav-maps
cd examples/backend/http-api-server
python3 app.py
```

`NXNAV_MAPS_DIR` tells the example server where to read map files. The product
default is usually `/var/lib/nxdog/nxnav-maps`.

Quick checks:

```bash
curl http://localhost:5088/nav_health
curl http://localhost:5088/get_ready_flag
```

## Example Endpoints

The endpoint handlers in `examples/backend/http-api-server/app.py` include
docstrings with request and response details.

Common examples:

```bash
curl http://localhost:5088/maps
curl http://localhost:5088/odom
curl http://localhost:5088/color
curl -X POST http://localhost:5088/brightness \
  -H "Content-Type: application/json" \
  -d '{"brightness": 6}'
curl -X POST http://localhost:5088/set_sport_action \
  -H "Content-Type: application/json" \
  -d '{"sport_action": "RecoveryStand"}'
```

The example includes endpoints for map listing/loading, initial pose, velocity
commands, navigation goals, route computation, odometry, navigation health,
auto-charging, VUI light color/brightness, VUI volume, and platform sport
actions.

## Troubleshooting Hints

If Python cannot import `nxnav_msgs` or `nxdog_interfaces`, rebuild and source
the ROS 2 interfaces:

```bash
cd /home/unitree/nxdog-developer-kit
source /opt/ros/foxy/setup.bash
colcon build --base-paths interfaces --symlink-install
source install/setup.bash
```

If API calls do not complete, confirm that the robot navigation stack is
running and visible in the same ROS 2 domain:

```bash
ros2 topic list
ros2 service list
ros2 action list
```
