# final_project
ros2 commands for running the project:

build and source the environment: ~ colcon build,    ~source install/setup.bash

launch the gazebo simulation with the vessel world:  ~ros2 launch my_robot_bringup robot.launch.py

run corner detection:    ~ros2 run object_detection detect_corner_node

run slime detection node: ~ros2 run object_detection slime_detection node

run mapping node: ~ros2 run object_detection mapping_node

run hole detection node:   ~ros2 run object_detection hole_detection_bode


running the laser_detection_segments.py: 
cd /nakai_sim/src/object_detection/object_detection/laser_detection$
python3 laser_detection_segments.py 





