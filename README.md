# nxdog SDK

The nxdog SDK lets customer applications control the robot dog through local
ROS 2 integrations and an HTTP API. It covers nxnav ROS 2 navigation workflows
as well as selected platform hardware features, including front VUI light color
and brightness, VUI volume, charging control/status, and sport actions such as
standing up, sitting down, walking, and recovery stand. The SDK runs directly
on the dog's Jetson Orin NX; Docker is not required.

The repository contains three main parts:

- `interfaces/`: ROS 2 message, service, and action definitions used by nxnav.
- `api/`: the Flask HTTP API server that customer applications should call for
  navigation and platform-control endpoints.
- `docs/`: user guides for related product tools, including the nxmap mapping
  workflow.

This guide first explains how to connect your development PC to the dog, then
shows how to set up and run the SDK on the Jetson Orin NX.

## Connect to the Dog

The rear of the dog has two visible Ethernet ports. The upper port connects to
the Pi 5, and the lower port connects to the Jetson Orin NX. The rest of this
README refers to the Jetson Orin NX as `nx`.

<p align="center">
  <img src="./docs/images/ethernet-ports.png" alt="Rear Ethernet ports on the dog" style="width: 30%; max-width: 100%;" />
</p>

Recommended development flow:

1. Connect your PC directly to either the Pi 5 or `nx` with an Ethernet cable.
2. Configure your PC's Ethernet interface with a static IPv4 address on the
   `192.168.123.0/24` subnet:
   - IP address: `192.168.123.xxx`, where `xxx` is any unused value from `1` to `254`
   - Subnet mask: `255.255.255.0`
   - Gateway: `192.168.123.1`
3. SSH into the Pi 5 or `nx`:
   - Pi 5: `ssh nexuni@192.168.123.20`, password: `ingensys`
   - nx: `ssh unitree@192.168.123.18`, password: `123`
4. Connect both the Pi 5 and `nx` to the same local Wi-Fi network.

```bash
sudo systemctl restart NetworkManager

# List detected Wi-Fi networks.
sudo nmcli dev wifi list

# Connect to a Wi-Fi network.
sudo nmcli dev wifi connect "<wifi-ssid>" password "<wifi-password>"
```

5. Restore the direct Ethernet cable connection between the Pi 5 and `nx`.
6. Connect your PC to the same Wi-Fi network.

After these steps, your PC, `nx`, and the Pi 5 should all be on the same LAN.
You can then:

- SSH into either the Pi 5 or `nx` wirelessly.
- Open the security frontend in a browser at `https://<pi5-ip>`.
- Open the mapping frontend in a browser at `http://<nx-ip>:5089`.

The rest of this README assumes that commands are run on `nx`.

## Setup

SSH into `nx`, then clone the nxdog SDK into `/home/unitree`:

```bash
cd /home/unitree
git clone https://github.com/nexuni/nxdog-sdk.git nxdog-sdk
cd /home/unitree/nxdog-sdk
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

Source the nxdog SDK interfaces before running the HTTP API server:

```bash
source /opt/ros/foxy/setup.bash
source /home/unitree/nxdog-sdk/install/setup.bash
```

You can verify that the generated interfaces are available with:

```bash
ros2 interface show nxnav_msgs/action/NavigateToPose
ros2 interface show nxdog_interfaces/srv/SportCommand
```

## Run the HTTP API Server

Use the HTTP endpoints in `api/app.py` as the nxdog SDK interface. The Flask server
listens on port `5088`.

```bash
cd /home/unitree/nxdog-sdk
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

## Use the HTTP Endpoints

Customer applications should integrate with the HTTP endpoints exposed by
`api/app.py`. Each endpoint handler includes a docstring that describes what it
does, the request JSON format, and the expected response.

Examples:

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

The API includes endpoints for map listing/loading, initial pose, velocity
commands, navigation goals, route computation, odometry, navigation health,
auto-charging, VUI light color/brightness, and platform sport actions.

## Mapping Guides

The mapping frontend is available at `http://<nx-ip>:5089` when nxmap is
running. See [docs/mapping-quick-start-guide.md](docs/mapping-quick-start-guide.md)
for the beginner nxmap workflow, including SLAM capture, point-cloud cleanup,
2D navigation map generation, PRM graph generation, and map bundle export.

## Troubleshooting

If Python cannot import `nxnav_msgs` or `nxdog_interfaces`, rebuild and source
the nxdog SDK interfaces:

```bash
cd /home/unitree/nxdog-sdk
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
