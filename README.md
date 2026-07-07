# nxdog Developer Kit

This repository provides public customer-facing documentation and reference
integration examples for the nxdog security patrol robot.

It is intended to help customers understand how to connect to the robot, use
the product tools, and build their own integrations around the robot-side
services.

## What Is Included

- Product setup and connection guides.
- nxmap mapping workflow documentation.
- Security frontend user guide and screenshots.
- Example HTTP backend integration code.
- ROS 2 message, service, and action definitions that match the robot-side
  nxnav and platform driver APIs.

The HTTP backend example was extracted from internal robot-side services and
trimmed to show common integration patterns. It is not a drop-in production SDK
and may need adaptation for each deployment. The ROS 2 interfaces are the
public compatibility definitions for the robot-side services.

## Repository Layout

```text
examples/
  backend/
    http-api-server/      Example Flask server for robot integration patterns.

interfaces/
  nxnav_msgs/             ROS 2 interfaces accepted by nxnav.
  nxdog_interfaces/       ROS 2 interfaces accepted by the platform driver.

docs/
  getting-started/
    connect-to-dog.md     Network and SSH connection guide.
  integration/
    example-backend.md    Reference setup and usage notes for the example code.
    ros2-interfaces.md    Notes for the ROS 2 interface contract.
  mapping/
    mapping-quick-start-guide.md
  security-frontend/      Security frontend user guide and images.
```

## Start Here

1. Connect your development PC to the robot:
   [docs/getting-started/connect-to-dog.md](docs/getting-started/connect-to-dog.md)
2. Review the example backend integration:
   [docs/integration/example-backend.md](docs/integration/example-backend.md)
3. Review the ROS 2 interface definitions:
   [docs/integration/ros2-interfaces.md](docs/integration/ros2-interfaces.md)
4. Review the nxmap beginner mapping workflow:
   [docs/mapping/mapping-quick-start-guide.md](docs/mapping/mapping-quick-start-guide.md)
5. Review the security frontend user guide:
   [docs/security-frontend/security-frontend-user-guide.md](docs/security-frontend/security-frontend-user-guide.md)

## Product Tool URLs

After your PC, the Jetson Orin NX, and the Pi 5 are on the same LAN:

- Security frontend: `https://<pi5-ip>`
- Mapping frontend: `http://<nx-ip>:5089`
- Example backend HTTP API: `http://<nx-ip>:5088`

## Notes

- The example backend assumes access to the robot's nxnav and platform ROS 2
  topics, services, and actions.
- The `interfaces/` packages are compatibility definitions for the robot-side
  ROS 2 APIs, not sample-only message shapes.
- The dependency commands in the integration guide are a starting point, not a
  fully validated installer.
- Product-specific manuals should live under `docs/`; runnable or copyable
  integration examples should live under `examples/`.
