# Backend Examples

This directory contains reference backend integration examples for the nxdog
security patrol robot.

- `http-api-server/`: example Flask server that exposes selected robot
  navigation and platform controls over HTTP.

The HTTP backend example depends on the ROS 2 interface packages in
`../../interfaces/`. The backend code is a template, not a production-supported
SDK. See `../../docs/integration/example-backend.md` for setup and usage notes.
