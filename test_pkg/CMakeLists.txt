cmake_minimum_required(VERSION 3.0.2)
project(test_pkg)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  std_srvs
  message_generation
)

add_message_files(
 DIRECTORY msg
 FILES
 myMsg.msg
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
