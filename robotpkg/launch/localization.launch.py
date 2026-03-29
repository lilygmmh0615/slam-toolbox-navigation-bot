from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

NAV2_PARAMS = '/workspaces/Robot/nav2_params.yaml'
MAP = '/workspaces/Robot/my_map.yaml'


def generate_launch_description():
    localization = TimerAction(
        period=2.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(get_package_share_directory('nav2_bringup'),
                                 'launch', 'localization_launch.py')
                ),
                launch_arguments={
                    'use_sim_time': 'true',
                    'params_file': NAV2_PARAMS,
                    'map': MAP,
                }.items(),
            )
        ],
    )

    goal_relay = Node(
        package='topic_tools',
        executable='relay',
        arguments=['/move_base_simple/goal', '/goal_pose'],
        output='screen',
    )

    nav2 = TimerAction(
        period=5.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(get_package_share_directory('nav2_bringup'),
                                 'launch', 'navigation_launch.py')
                ),
                launch_arguments={
                    'use_sim_time': 'true',
                    'params_file': NAV2_PARAMS,
                }.items(),
            )
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),
        localization,
        goal_relay,
        nav2,
    ])
