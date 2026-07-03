"""
nxnav_client
============

Platform-independent Python client for the nxnav navigation stack.

Quick start::

    from nxnav_client import NxNavClient, NavGoal

    nav = NxNavClient(config_path="/path/to/nxnav_params.yaml")
    nav.start()

    nav.goto(NavGoal(map_name="floor6", x=5.0, y=3.0, yaw=1.57))
    print(nav.get_pose())

    nav.stop()
"""

from nxnav_client import NxNavClient
from nav_types import (
    MapInfo,
    NavGoal,
    NavPlan,
    NavResult,
    NavResultCode,
    Pose2D,
    Pose3D,
    Portal,
    Velocity,
    Zone,
)

__all__ = [
    "NxNavClient",
    "MapInfo",
    "NavGoal",
    "NavPlan",
    "NavResult",
    "NavResultCode",
    "Pose2D",
    "Pose3D",
    "Portal",
    "Velocity",
    "Zone",
]
