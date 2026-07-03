# One segment of a cross-map navigation route.
# A route is a sequence of segments, each crossing one portal.
string src_map                            # Map tile to navigate on
string portal_name                        # Portal identifier in the map graph
string portal_type                        # level, stair-up, stair-down, elevator
string dst_map                            # Destination map tile after crossing
geometry_msgs/Pose exit_pose              # Pose to navigate to before portal
float64 exit_tolerance_xy 0.3
float64 exit_tolerance_yaw 10.0
geometry_msgs/Point[] pre_switch_path     # Path before map switch (stair-up, elevator-in)
geometry_msgs/Point[] post_switch_path    # Path after map switch (stair-down, elevator-out)
bool disable_avoidance false              # Disable collision avoidance during portal path
