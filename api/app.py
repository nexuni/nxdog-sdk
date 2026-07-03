import os
import logging
import re
import math
import threading

from flask import Flask, request, jsonify
from flask_cors import CORS

from nxnav_client import NavGoal, NavPlan, NxNavClient
from platform_driver_client import NxDogPlatformClient

_MAPS_DIR = os.getenv('NXNAV_MAPS_DIR', '/var/lib/nxdog/nxnav-maps')

logger = logging.getLogger('werkzeug')
logger.disabled = True

app = Flask(__name__, static_url_path='/static')
CORS(app)

TILE_SIZE_METER = 100.0

api = NxNavClient()
api.start()

@app.route('/maps', methods=['GET'])
def get_available_maps():
    """
    Lists available map groups from NXNAV_MAPS_DIR.
    Behavior: scans map_graph-<name>.json files and map directories containing
    matching graph files.
    Request JSON: none.
    Response: {"maps": [<map_name>, ...]} or {"error": <message>} on failure.
    """
    pattern = re.compile(r'^map_graph-(.+)\.json$')
    map_names = set()
    try:
        for filename in os.listdir(_MAPS_DIR):
            match = pattern.match(filename)
            if match:
                map_names.add(match.group(1))
                continue
            map_dir = os.path.join(_MAPS_DIR, filename)
            if os.path.isdir(map_dir):
                graph_path = os.path.join(map_dir, f'map_graph-{filename}.json')
                if os.path.exists(graph_path):
                    map_names.add(filename)
    except FileNotFoundError:
        map_names = []
    except Exception as e:
        print(f"[ERROR] Failed to list maps: {e}")
        return jsonify({"error": str(e)}), 500
    return jsonify({"maps": sorted(map_names)})

@app.route('/set_initialpose', methods=['POST'])
def set_initialpose():
    """
    Sets the robot initial pose and switches to the tile map for that pose.
    Behavior: converts the pose quaternion to yaw, sets the map, then publishes
    the initial pose.
    Request JSON: {"map": <map_name>, "position": [x, y, z],
    "orientation": [qx, qy, qz, qw]}.
    Response: {"status": "success"} or an error/status object on failure.
    """
    data = request.get_json()
    position = data.get("position")
    orientation = data.get("orientation")
    map_name = data.get("map")
    if not map_name:
        return jsonify({"error": "map is required"}), 400
    x, y, yaw = _pose_to_xy_yaw(position, orientation)
    tile_name = _pos_to_tile_name(map_name, x, y)

    map_ev = threading.Event()
    map_res = False

    def map_callback(result):
        nonlocal map_res
        map_res = result
        map_ev.set()
        return

    api.set_map(str(map_name), result_callback=map_callback)
    map_ev.wait(timeout=30)
    if map_res == False:
        return jsonify({"status": "fail set_map", "map": map_name, "map_tile": tile_name}), 500

    api.set_initialpose(x, y, yaw, tile_name)
    return jsonify({"status": "success"})

@app.route('/set_cmd_vel', methods=['POST'])
def set_cmd_vel():
    """
    Sends a velocity command to the robot.
    Behavior: publishes vx, vy, and wz using the mid-speed command channel.
    Request JSON: {"vx": <float>, "vy": <float>, "wz": <float>}.
    Response: {"status": "success"}.
    """
    data = request.get_json()
    vx = float(data.get("vx"))
    vy = float(data.get("vy"))
    wz = float(data.get("wz"))
    api.set_cmd_vel(vx, vy, wz, 'mid')
    return jsonify({"status": "success"})

@app.route('/get_ready_flag', methods=['GET'])
def get_ready_flag():
    """
    Reports whether nxnav is ready.
    Behavior: reads the current ready flag from the navigation client.
    Request JSON: none.
    Response: {"ready_flag": <bool>}.
    """
    return jsonify({"ready_flag": api.is_ready()})

@app.route('/pause', methods=['GET'])
def robot_pause():
    """
    Pauses the active navigation task.
    Behavior: sends a pause request to nxnav.
    Request JSON: none.
    Response: {"status": "success pause"}.
    """
    api.pause()
    return jsonify({"status": "success pause"})

@app.route('/stop', methods=['GET'])
def robot_stop():
    """
    Stops the active navigation task.
    Behavior: cancels the current nxnav goal.
    Request JSON: none.
    Response: {"status": "success stop"}.
    """
    api.cancel()
    return jsonify({"status": "success stop"})

@app.route('/resume', methods=['GET'])
def robot_resume():
    """
    Resumes a paused navigation task.
    Behavior: sends a resume request to nxnav.
    Request JSON: none.
    Response: {"status": "success resume"}.
    """
    api.resume()
    return jsonify({"status": "success resume"})

@app.route('/navigate', methods=['POST'])
def robot_navigate():
    """
    Navigates the robot to a target pose.
    Behavior: converts the target pose to a tiled NavGoal, sends it to nxnav,
    and waits for completion or timeout.
    Request JSON: {"map": <map_group>, "position": [x, y, z],
    "orientation": [qx, qy, qz, qw], "goal_tolerance_xy": <float optional>,
    "goal_tolerance_yaw": <float optional>}.
    Response: {"message": <result>, "status": <status_code>}.
    """
    data = request.get_json()
    position = data.get("position")
    orientation = data.get("orientation")
    goal_tolerance_xy = data.get("goal_tolerance_xy", 0.3)
    goal_tolerance_yaw = data.get("goal_tolerance_yaw", 0.1)
    map_name = data.get("map")

    if goal_tolerance_xy is None: goal_tolerance_xy = 0.3
    if goal_tolerance_yaw is None: goal_tolerance_yaw = 0.1

    nav_goal = _goal_dict_to_nav_goal({
        'position': [float(p) for p in position],
        'orientation': [float(p) for p in orientation],
        'goal_tolerance_xy': float(goal_tolerance_xy),
        'goal_tolerance_yaw': float(goal_tolerance_yaw),
        'map_name': map_name
    })

    ev = threading.Event()
    res = False
    status = -1

    def nav_result_callback(nav_result):
        nonlocal res, status
        status = nav_result.status_code
        res = nav_result.success
        ev.set()
        return

    api.goto(nav_goal, result_callback=nav_result_callback)
    ev.wait(timeout=600)

    if res == False:
        return jsonify({"message": "fail navigate", "status": status}), 500
    return jsonify({"message": "success navigate", "status": status})

@app.route('/current_map', methods=['GET'])
def get_current_map():
    """
    Returns the current map group.
    Behavior: reads the active tile map and strips the tile suffix.
    Request JSON: none.
    Response: {"current_map": <map_group_or_null>}.
    """
    return jsonify({"current_map": _get_map_group(api.get_current_map())})

@app.route('/odom', methods=['GET'])
def get_odom():
    """
    Returns the robot odometry pose.
    Behavior: reads x, y, yaw, current map group, and current map tile.
    Request JSON: none.
    Response: {"odom": {"x": <float>, "y": <float>, "yaw": <float>,
    "map": <map_group_or_null>, "map_tile": <tile_or_null>}}.
    """
    pose = api.get_pose()
    return jsonify({
        "odom": {
            "x": pose.x,
            "y": pose.y,
            "yaw": pose.yaw,
            "map": _get_map_group(api.get_current_map()),
            "map_tile": api.get_current_map(),
        }
    })

@app.route('/nav_plan', methods=['GET'])
def get_nav_plan():
    """
    Returns the current navigation plan.
    Behavior: reads the active plan from nxnav and converts NavPlan objects to
    JSON-friendly dictionaries.
    Request JSON: none.
    Response: {"nav_plan": {"map": <map_group>, "path": <path>} or raw plan}.
    """
    return jsonify({"nav_plan": _plan_to_dict(api.plan())})

@app.route('/compute_route', methods=['POST'])
def compute_route():
    """
    Computes a route through one or more target goals.
    Behavior: converts each goal to a tiled NavGoal and asks nxnav to compute
    the route without starting navigation.
    Request JSON: {"goal": [{"map": <map_group>, "position": [x, y, z],
    "orientation": [qx, qy, qz, qw], "goal_tolerance_xy": <float optional>,
    "goal_tolerance_yaw": <float optional>, "nav_speed": <float optional>},
    ...]}.
    Response: {"route": [{"map": <map_group>, "path": <path>}]} or
    {"route": [[]]} when no goals are provided.
    """
    data = request.get_json()
    goals = data.get("goal")
    if goals is None:
        route = []
    else:
        nav_goals = [_goal_dict_to_nav_goal(goal) for goal in goals]
        route = {
            "map": goals[0]["map"],
            "path": api.compute_route(nav_goals),
        }
    return jsonify({"route": [route]})

@app.route('/velocity', methods=['GET'])
def get_velocity():
    """
    Returns the current robot velocity.
    Behavior: reads vx, vy, and wz, zeroing small vx/vy noise below 0.05.
    Request JSON: none.
    Response: {"level": [vx, vy, wz]}.
    """
    vel = api.get_velocity()
    return jsonify({"level": [
        vel.vx if abs(vel.vx) > 0.05 else 0.0,
        vel.vy if abs(vel.vy) > 0.05 else 0.0,
        vel.wz,
    ]})

@app.route('/nav_health', methods=['GET'])
def get_nav_health():
    """
    Reports whether the nxnav client is alive.
    Behavior: checks the navigation client's health state.
    Request JSON: none.
    Response: {"alive": <bool>}.
    """
    return jsonify({"alive": api.is_alive()})








# ---------- platform driver related api -------------

api_pd = NxDogPlatformClient()
api_pd.start()

@app.route('/map', methods=['POST'])
def set_map():
    """
    Switches the active navigation map.
    Behavior: accepts either a raw JSON string map name or an object containing
    map_name, map, or name, then waits for nxnav to finish switching maps.
    Request JSON: "<map_name>" or {"map_name": <map_name>} or
    {"map": <map_name>} or {"name": <map_name>}.
    Response: {"status": "success set_map", "map": <map_name>} or an
    error/status object on failure.
    """
    data = request.get_json(force=True, silent=True)
    if isinstance(data, str):
        map_name = data
    elif isinstance(data, dict):
        map_name = data.get("map_name") or data.get("map") or data.get("name")
    else:
        map_name = None

    if not map_name:
        return jsonify({"error": "map name is required"}), 400

    ev = threading.Event()
    res = False

    def result_callback(result):
        nonlocal res
        res = result
        ev.set()
        return

    api.set_map(str(map_name), result_callback=result_callback)
    ev.wait(timeout=30)
    if res == False:
        return jsonify({"status": "fail set_map", "map": map_name}), 500
    return jsonify({"status": "success set_map", "map": map_name})

@app.route('/charging', methods=['POST'])
def start_charging():
    """
    Starts the auto-charging behavior.
    Behavior: sends an auto-charge start request to the platform driver and
    waits for the result.
    Request JSON: none.
    Response: {"status": "success start_charging"} or failure status.
    """
    ev = threading.Event()
    res = False
    def result_callback(result):
        print(f'[start_charging()] start charging result: {result}.')
        ev.set()
        nonlocal res
        res = result
        return
    api_pd.auto_charging_start(result_callback)
    ev.wait(timeout=360)
    if res == False:
        return jsonify({"status": "fail start_charging"}), 500
    return jsonify({"status": "success start_charging"})

@app.route('/auto_charging_stop', methods=['POST'])
def auto_charging_stop():
    """
    Stops the auto-charging behavior.
    Behavior: sends an auto-charge stop request to the platform driver and
    waits for the result.
    Request JSON: none.
    Response: {"status": "success auto_charging_stop"} or failure status.
    """
    ev = threading.Event()
    res = False
    def result_callback(result):
        print(f'[auto_charging_stop()] stop charging result: {result}.')
        ev.set()
        nonlocal res
        res = result
        return
    api_pd.auto_charging_stop(result_callback)
    ev.wait(timeout=30)
    if res == False:
        return jsonify({"status": "fail auto_charging_stop"}), 500
    return jsonify({"status": "success auto_charging_stop"})

@app.route('/is_charging', methods=["GET"])
def is_charging():
    """
    Reports whether the robot is charging.
    Behavior: reads charging state from the platform driver.
    Request JSON: none.
    Response: {"is_charging": <bool>}.
    """
    charging = api_pd.is_charging()
    return jsonify({"is_charging": charging})
    
@app.route('/color', methods=['GET'])
def get_color():
    """
    Returns the current VUI LED color.
    Behavior: reads color state from the platform driver.
    Request JSON: none.
    Response: {"color": <color_value>}.
    """
    color = api_pd.vui_get_color()
    return jsonify({"color": color})

@app.route('/color', methods=['POST'])
def set_color():
    """
    Sets the VUI LED color.
    Behavior: forwards the requested color value to the platform driver.
    Request JSON: {"color": <color_value>}.
    Response: {"status": "success"}.
    """
    data = request.get_json()
    color = data.get("color")
    api_pd.vui_set_color(color)
    return jsonify({"status": "success"})

@app.route('/brightness', methods=['GET'])
def get_brightness():
    """
    Returns the current VUI LED brightness.
    Behavior: reads brightness state from the platform driver.
    Request JSON: none.
    Response: {"brightness": <brightness_value>}.
    """
    brightness = api_pd.vui_get_brightness()
    return jsonify({"brightness": brightness})

@app.route('/brightness', methods=['POST'])
def set_brightness():
    """
    Sets the VUI LED brightness.
    Behavior: forwards the requested brightness value to the platform driver.
    Request JSON: {"brightness": <brightness_value>}.
    Response: {"status": "success"}.
    """
    data = request.get_json()
    brightness = data.get("brightness")
    api_pd.vui_set_brightness(brightness)
    return jsonify({"status": "success"})

@app.route('/set_sport_action', methods=['POST'])
def set_sport_action():
    """
    Triggers a platform sport action.
    Behavior: forwards the requested sport action value to the platform driver.
    Request JSON: {"sport_action": <action_value>}.
    Response: {"status": "success"}.
    """
    data = request.get_json()
    sport_action = data.get("sport_action")
    print(f'[set_sport_action()] sport_action: {sport_action}')
    api_pd.set_sport_action(sport_action)
    return jsonify({"status": "success"})


def _goal_dict_to_nav_goal(goal):
    x, y, yaw = _pose_to_xy_yaw(goal["position"], goal["orientation"])
    map_name = goal.get("map_name") or goal.get("map") or ""
    assert map_name != ""
    map_name = _pos_to_tile_name(map_name, x, y)
    return NavGoal(
        map_name=map_name,
        x=x,
        y=y,
        yaw=yaw,
        goal_tolerance_xy=float(goal.get("goal_tolerance_xy", 0.3)),
        goal_tolerance_yaw=float(goal.get("goal_tolerance_yaw", 0.1)),
        nav_speed=float(goal.get("nav_speed", 1.25)),
    )


def _pose_to_xy_yaw(position, orientation):
    return float(position[0]), float(position[1]), _quat_to_yaw(orientation)


def _quat_to_yaw(orientation):
    qx = float(orientation[0])
    qy = float(orientation[1])
    qz = float(orientation[2])
    qw = float(orientation[3])
    return math.atan2(
        2.0 * (qw * qz + qx * qy),
        1.0 - 2.0 * (qy * qy + qz * qz),
    )


def _plan_to_dict(plan):
    if isinstance(plan, NavPlan):
        return {
            "map": _get_map_group(plan.map_name),
            "path": plan.path,
        }
    return plan


def _pos_to_tile_name(map_group_name, x, y):
    tx = math.floor(float(x) / TILE_SIZE_METER)
    ty = math.floor(float(y) / TILE_SIZE_METER)
    tx_str = f"p{abs(tx)}" if tx >= 0 else f"n{abs(tx)}"
    ty_str = f"p{abs(ty)}" if ty >= 0 else f"n{abs(ty)}"
    return f"{map_group_name}_{tx_str}_{ty_str}"


def _get_map_group(map_name):
    if map_name is None:
        return None
    return map_name.split("_")[0]


if __name__ == '__main__':
    # Initialize database on startup
    try:
        logger.info("Starting nxnav API server...")
        app.run(host='0.0.0.0', port=5088, debug=False, threaded=True)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down...")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise
    finally:
        logger.info("Stopping api...")
        api.stop()
        api_pd.stop()
