cmake_minimum_required(VERSION 3.0.2)
project(path_following)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  std_srvs
  message_generation
)

generate_messages(
 DEPENDENCIES
 std_msgs
)


catkin_package(
 CATKIN_DEPENDS
 std_msgs
 message_runtime
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
