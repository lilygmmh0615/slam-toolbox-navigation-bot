### Build (when setup.py is changed)
```
colcon build --packages-select robotpkg && source install/setup.bash
```

### Run foxglove visualization
```
sudo apt install -y ros-humble-foxglove-bridge (run once per new container)

ros2 launch foxglove_bridge foxglove_bridge_launch.xml use_sim_time:=true
```

foxglove connect to,
`ws://127.0.0.1:8765`

### Launch gazebo simulation,
```
ros2 launch robotpkg gazebo.launch.py
```

### Launch slam
Launch slam in either mapping mode or localization mode

* Launch slam mapping mode,
(change slam.config.yaml mode and slam.launch.py executable)
    ```
    ros2 launch robotpkg slam.launch.py
    ```

* Launch slam localization mode,
(change slam.config.yaml mode and slam.launch.py executable)
    ```
    ros2 launch robotpkg localization.launch.py
    ```

slam mapping mode save map,
```
ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph "{filename: '/workspaces/Robot/my_map'}"
```

slam localization mode save map,
```
ros2 run nav2_map_server map_saver_cli -f /workspaces/Robot/my_map --ros-args -p save_map_timeout:=10.0
```
or `save_map.sh`

### Use keyboard to drive the robot
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard  --ros-args --remap use_sim_time:=true
```

### Testing
post a 2D goal on foxglove and watch the robot move there. It will also avoid adhoc obstacles.

drop an obstacle
```
ros2 run gazebo_ros spawn_entity.py -entity obstacle_box_5 -x -0.83 -y -7.28 -z 0.5 -stdin << 'EOF'
<sdf version='1.6'>
  <model name='obstacle_box'>
    <static>true</static>
    <link name='link'>
      <collision name='collision'><geometry><box><size>3.5 3.5 1.0</size></box></geometry></collision>
      <visual name='visual'><geometry><box><size>3.5 3.5 1.0</size></box></geometry></visual>
    </link>
  </model>
</sdf>
EOF
```