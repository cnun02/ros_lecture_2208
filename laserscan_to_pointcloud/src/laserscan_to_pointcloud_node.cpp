#include "laserscan_to_pointcloud/laserscan_to_pointcloud.h"

int main(int argc, char **argv)
{
  ros::init(argc, argv, "laserscan_to_pointcloud");
  ros::NodeHandle nh("");
  ros::NodeHandle pnh("~");

  laserscan_to_pointcloud::LaserscanToPointcloud converter(nh,pnh);
  ros::spin();
  return 0;
}
