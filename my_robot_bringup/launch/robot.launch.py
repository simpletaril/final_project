from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from ament_index_python.packages import get_package_share_directory
import os
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Define paths for URDF and RViz configuration
    urdf_path = LaunchConfiguration('urdf_path')
    rviz_config_path = LaunchConfiguration('rviz_config_path')
    pkg_share = FindPackageShare(package='my_robot_bringup').find('my_robot_bringup')
    robot_localization_file_path = os.path.join(pkg_share, 'config/ekf.yaml')

    # Declare use_sim_time argument
    use_sim_time = LaunchConfiguration('use_sim_time')

    return LaunchDescription([
        # Declare arguments for URDF and RViz configuration paths
        DeclareLaunchArgument(
            'urdf_path',
            default_value=[get_package_share_directory('my_robot_description') + '/urdf/my_robot.urdf.xacro'],
            description='Path to the URDF file'
        ),
        DeclareLaunchArgument(
            'rviz_config_path',
            default_value=[get_package_share_directory('my_robot_bringup') + '/rviz/urdf_config.rviz'],
            description='Path to the RViz configuration file'
        ),
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='True',
            description='Use simulation (Gazebo) clock if true'
        ),

        # Launch the robot_state_publisher node
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': Command(['xacro ', urdf_path])
            }]
        ),

        # Launch Gazebo with the specified world
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                get_package_share_directory('gazebo_ros') + '/launch/gazebo.launch.py'
            ]),
            launch_arguments={'world': get_package_share_directory('my_robot_bringup') + '/worlds/sea.world'}.items()   #  model without textures 'cliff'  change world file name
        ),

        # Spawn the robot entity in Gazebo with a specific orientation
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='spawn_entity',
            output='screen',
            arguments=[
                '-topic', '/robot_description',
                '-entity', 'my_robot',
                '-x', '0', '-y', '0', '-z', '4',
                '-R', '-1.57', '-P', '0', '-Y', '0'
            ],
            remappings=[('/robot_description', '/robot_description')]
        ),

        # Launch RViz with the specified configuration
        Node(
            package='rviz2',
            executable='rviz2',
            output='screen',
            arguments=['-d', rviz_config_path]
        ),

        # Launch the force_applier node
        Node(
            package='my_robot_simulation',
            executable='force_applier',
            output='screen',
            # Add parameters or remappings if needed
        ),

        # Launch the joint_state_publisher_gui node
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen',
            parameters=[{
                'robot_description': Command(['xacro ', urdf_path])
            }]
        ),

        # Start robot localization using an Extended Kalman filter
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[robot_localization_file_path, 
            {'use_sim_time': use_sim_time}]  # Correctly use LaunchConfiguration here
        ),

        # Launch the mapping node
        Node(
            package='object_detection',
            executable='mapping_node',
            output='screen',
            # Add parameters or remappings if needed
        ),

        # Launch the hole detection node
        Node(
            package='object_detection',
            executable='hole_detection_node',
            output='screen',
            # Add parameters or remappings if needed
        ),

        # Launch the slime detection node
        Node(
            package='object_detection',
            executable='slime_detection_node',
            output='screen',
            # Add parameters or remappings if needed
        ),

        Node(
            package='obstacle_avoidance',
            executable='teleop_gui_node',
            output='screen',
        ),


         Node(
            package='imu_pkg',
            executable='complementary_filter_node',
            output='screen',
            # Add parameters or remappings if needed
        ),
       

    ])



















# from launch import LaunchDescription
# from launch_ros.actions import Node
# from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch.substitutions import LaunchConfiguration, Command
# from ament_index_python.packages import get_package_share_directory
# import os
# from launch_ros.substitutions import FindPackageShare

# def generate_launch_description():
#     # Define paths for URDF and RViz configuration
#     urdf_path = LaunchConfiguration('urdf_path')
#     rviz_config_path = LaunchConfiguration('rviz_config_path')
#     pkg_share = FindPackageShare(package='my_robot_bringup').find('my_robot_bringup')
#     robot_localization_file_path = os.path.join(pkg_share, 'config/ekf.yaml')

#     # Declare use_sim_time argument
#     use_sim_time = LaunchConfiguration('use_sim_time')

#     return LaunchDescription([
#         # Declare arguments for URDF and RViz configuration paths
#         DeclareLaunchArgument(
#             'urdf_path',
#             default_value=[get_package_share_directory('my_robot_description') + '/urdf/my_robot.urdf.xacro'],
#             description='Path to the URDF file'
#         ),
#         DeclareLaunchArgument(
#             'rviz_config_path',
#             default_value=[get_package_share_directory('my_robot_bringup') + '/rviz/urdf_config.rviz'],
#             description='Path to the RViz configuration file'
#         ),
#         DeclareLaunchArgument(
#             'use_sim_time',
#             default_value='True',
#             description='Use simulation (Gazebo) clock if true'
#         ),

#         # Launch the robot_state_publisher node
#         Node(
#             package='robot_state_publisher',
#             executable='robot_state_publisher',
#             output='screen',
#             parameters=[{
#                 'robot_description': Command(['xacro ', urdf_path])
#             }]
#         ),

#         # Launch Gazebo with the specified world
#         IncludeLaunchDescription(
#             PythonLaunchDescriptionSource([
#                 get_package_share_directory('gazebo_ros') + '/launch/gazebo.launch.py'
#             ]),
#             launch_arguments={'world': get_package_share_directory('my_robot_bringup') + '/worlds/sea.world'}.items()   # change world file name
#         ),

#         # Spawn the robot entity in Gazebo with a specific orientation
#         Node(
#             package='gazebo_ros',
#             executable='spawn_entity.py',
#             name='spawn_entity',
#             output='screen',
#             arguments=[
#                 '-topic', '/robot_description',
#                 '-entity', 'my_robot',
#                 '-x', '0', '-y', '0', '-z', '4',
#                 '-R', '-1.57', '-P', '0', '-Y', '0'
#             ],
#             remappings=[('/robot_description', '/robot_description')]
#         ),

#         # Launch RViz with the specified configuration
#         Node(
#             package='rviz2',
#             executable='rviz2',
#             output='screen',
#             arguments=['-d', rviz_config_path]
#         ),

#         # Launch the force_applier node
#         Node(
#             package='my_robot_simulation',
#             executable='force_applier',
#             output='screen',
#             # Add parameters or remappings if needed
#         ),

#         # Launch the joint_state_publisher_gui node
#         Node(
#             package='joint_state_publisher_gui',
#             executable='joint_state_publisher_gui',
#             output='screen',
#             parameters=[{
#                 'robot_description': Command(['xacro ', urdf_path])
#             }]
#         ),

#         # Start robot localization using an Extended Kalman filter
#         Node(
#             package='robot_localization',
#             executable='ekf_node',
#             name='ekf_filter_node',
#             output='screen',
#             parameters=[robot_localization_file_path, 
#             {'use_sim_time': use_sim_time}]  # Correctly use LaunchConfiguration here
#         )
#     ])



