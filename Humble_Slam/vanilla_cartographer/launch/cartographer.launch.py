#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    start_rviz = LaunchConfiguration('start_rviz')
    use_sim = LaunchConfiguration('use_sim')

    cartographer_config_dir = PathJoinSubstitution(
        [
            FindPackageShare('vanilla_cartographer'),
            'config',
        ]
    )
    configuration_basename = LaunchConfiguration('configuration_basename')

    resolution = LaunchConfiguration('resolution')

    rviz_config_file = PathJoinSubstitution(
        [
            FindPackageShare('vanilla_cartographer'),
            'rviz',
            'cartographer.rviz'
        ]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'start_rviz',
            default_value='true',
            description='Whether execute rviz2'),

        DeclareLaunchArgument(
            'use_sim',
            default_value='true',
            description='Start robot in Gazebo simulation'),

        DeclareLaunchArgument(
            'cartographer_config_dir',
            default_value=cartographer_config_dir,
            description='Full direction of config file'),

        DeclareLaunchArgument(
            'configuration_basename',
            default_value='vanilla.lua',
            description='Name of lua file for cartographer'),

        DeclareLaunchArgument(
            'resolution',
            default_value='0.05',
            description='Resolution of a grid cell of occupancy grid'),

        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim}],
            arguments=['-configuration_directory', cartographer_config_dir,
                       '-configuration_basename', configuration_basename]),

        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim}],
            arguments=['-resolution', resolution]),

        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config_file],
            output='screen',
            condition=IfCondition(start_rviz)),
    ])