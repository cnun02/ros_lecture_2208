cmake_minimum_required(VERSION 2.8.3)
project(laserscan_to_pointcloud)

find_package(catkin_simple REQUIRED)
catkin_simple(ALL_DEPS_REQUIRED)

add_definitions(-std=c++11 -Wall -Wextra)

cs_add_executable(laserscan_to_pointcloud
	src/laserscan_to_pointcloud_node.cpp
	src/laserscan_to_pointcloud.cpp
	include/laserscan_to_pointcloud/laserscan_to_pointcloud.h
)
target_link_libraries(${PROJECT_NAME} ${catkin_LIBRARIES})
