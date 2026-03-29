from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction
from launch_ros.actions import Node

URDF = '/workspaces/Robot/my_robot.urdf'
WORLD = '/workspaces/Robot/world.sdf'

with open(URDF, 'r') as f:
    robot_description = f.read()


def generate_launch_description():
    gazebo = ExecuteProcess(
        cmd=['gzserver', '--verbose', WORLD, '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'],
        additional_env={'GAZEBO_PLUGIN_PATH': '/opt/ros/humble/lib'},
        output='screen',
    )

    spawn_robot = TimerAction(
        period=3.0,
        actions=[
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                arguments=['-entity', 'my_robot', '-file', URDF],
                parameters=[{'use_sim_time': True}],
                output='screen',
            )
        ],
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True,
            'publish_frequency': 10.0,
        }],
        output='screen',
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),
        gazebo,
        robot_state_publisher,
        spawn_robot,
    ])
