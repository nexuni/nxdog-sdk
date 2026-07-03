# nxnav SDK

This SDK lets customer applications control the nxnav ROS 2 navigation stack
through a local HTTP API. It is intended to run directly on the robot host;
Docker is not required.

The repository contains two main parts:

- `interfaces/`: ROS 2 message, service, and action definitions used by nxnav.
- `api/`: the Flask HTTP API server that customer applications should call.

## Setup

Clone the SDK into `/home/unitree`, then enter the repository:

```bash
cd /home/unitree
git clone <nxnav-sdk-repo-url> nxnav-sdk
cd /home/unitree/nxnav-sdk
source /opt/ros/foxy/setup.bash
```

Install system dependencies:

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

Install Python dependencies:

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

Source the SDK interfaces before running the HTTP API server:

```bash
source /opt/ros/foxy/setup.bash
source /home/unitree/nxnav-sdk/install/setup.bash
```

You can verify that the generated interfaces are available with:

```bash
ros2 interface show nxnav_msgs/action/NavigateToPose
ros2 interface show nxdog_interfaces/srv/SportCommand
```

## Run The HTTP API Server

Use the HTTP endpoints in `api/app.py` as the SDK interface. The Flask server
listens on port `5088`.

```bash
cd /home/unitree/nxnav-sdk
source /opt/ros/foxy/setup.bash
source install/setup.bash
cd api
python3 app.py
```

Recommended map directory:

```bash
export NXNAV_MAPS_DIR=/var/lib/nxdog/nxnav-maps
```

`NXNAV_MAPS_DIR` tells the server where to read map files. We recommend
`/var/lib/nxdog/nxnav-maps`, which is the default map storage location for the
product.

Quick health check:

```bash
curl http://localhost:5088/nav_health
curl http://localhost:5088/get_ready_flag
```

## Use The HTTP Endpoints

Customer applications should integrate with the HTTP endpoints exposed by
`api/app.py`. Each endpoint handler includes a docstring that describes what it
does, the request JSON format, and the expected response.

Examples:

```bash
curl http://localhost:5088/maps
curl http://localhost:5088/odom
```

## Troubleshooting

If Python cannot import `nxnav_msgs` or `nxdog_interfaces`, rebuild and source
the SDK interfaces:

```bash
cd /home/unitree/nxnav-sdk
source /opt/ros/foxy/setup.bash
colcon build --base-paths interfaces --symlink-install
source install/setup.bash
```

If API calls do not complete, confirm that the robot navigation stack is running
and visible in the same ROS 2 domain:

```bash
ros2 topic list
ros2 service list
ros2 action list
```