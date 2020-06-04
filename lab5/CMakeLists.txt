cmake_minimum_required(VERSION 2.8.3)
project(lab5)

find_package(catkin REQUIRED COMPONENTS
  rospy
  urdf
  std_msgs
  message_generation
)

add_service_files(DIRECTORY srv
  FILES
  Jint.srv
  Oint.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(

  CATKIN_DEPENDS message_runtime std_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

