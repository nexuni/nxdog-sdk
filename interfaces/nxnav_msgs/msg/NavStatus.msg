uint8 STATUS_IDLE=0
uint8 STATUS_NAVIGATING=1
uint8 STATUS_PAUSED=2
uint8 STATUS_FOLLOWING_PATH=3
uint8 STATUS_RECOVERING=4

uint8 status
string current_map
geometry_msgs/Pose current_pose
float64 distance_remaining
