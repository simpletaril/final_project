cmake_minimum_required(VERSION 3.8)
project(imu_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)

# Add the executable
add_executable(complementary_filter_node src/imu_filter.cpp)

# Link dependencies
ament_target_dependencies(complementary_filter_node rclcpp sensor_msgs)

# Install the executable
install(TARGETS
  complementary_filter_node
  DESTINATION lib/${PROJECT_NAME})


ament_package()
