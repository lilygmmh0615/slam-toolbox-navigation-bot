from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

SLAM_CONFIG = '/workspaces/Robot/slam_config.yaml'
NAV2_PARAMS = '/workspaces/Robot/nav2_params.yaml'


def generate_launch_description():
    slam = TimerAction(
        period=2.0,
        actions=[
            Node(
                package='slam_toolbox',
                # for mapping use this,
                # executable='async_slam_toolbox_node',
                executable='localization_slam_toolbox_node',
                parameters=[SLAM_CONFIG, {'use_sim_time': True}],
                output='screen',
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
        slam,
        goal_relay,
        nav2,
    ])
