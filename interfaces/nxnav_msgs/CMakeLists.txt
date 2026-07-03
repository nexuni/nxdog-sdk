cmake_minimum_required(VERSION 3.5)
project(nxnav_msgs)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  # Messages
  "msg/NavStatus.msg"
  "msg/MapZone.msg"
  "msg/MapPath.msg"
  "msg/MapPose.msg"
  "msg/MapData.msg"
  "msg/RouteSegment.msg"
  # Services
  "srv/LoadMap.srv"
  "srv/SwitchMap.srv"
  "srv/ComputeRoute.srv"
  # Actions
  "action/ComputePath.action"
  "action/ComputePrmPath.action"
  "action/FollowPath.action"
  "action/NavigateToPose.action"
  "action/Recovery.action"
  DEPENDENCIES geometry_msgs nav_msgs
)

ament_package()
