#!/bin/bash
ros2 run nav2_map_server map_saver_cli -f /workspaces/Robot/my_map --ros-args -p save_map_timeout:=10.0
sed -i 's/free_thresh: 0.250000/free_thresh: 0.19/' /workspaces/Robot/my_map.yaml
echo "Map saved with free_thresh: 0.19"
