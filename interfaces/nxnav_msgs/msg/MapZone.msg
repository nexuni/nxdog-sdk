# A zone on a map with special navigation behavior.
# Zones are defined as polygons in the per-map JSON files.
string name
string type          # door, stair, elevator, config, map
geometry_msgs/Point[] polygon   # Vertices of the zone boundary polygon
string parameters_json           # JSON dict of parameter overrides (config zones)
