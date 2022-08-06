#pragma once

#include <iostream>
#include <vector>
#include <Eigen/Dense>

#include <ros/ros.h>

#include <sensor_msgs/PointCloud2.h>
#include <sensor_msgs/LaserScan.h>
#include <laser_geometry/laser_geometry.h>

#include <std_msgs/Empty.h>

namespace laserscan_to_pointcloud
{

class LaserscanToPointcloud
{
public:
  LaserscanToPointcloud(const ros::NodeHandle & nh, const ros::NodeHandle & pnh);
  ~LaserscanToPointcloud();

  void lidarCallback(const sensor_msgs::LaserScan::ConstPtr& msg);

private:
  ros::NodeHandle nh_;
  ros::NodeHandle pnh_;

  ros::Subscriber laser_scan_sub_;
  ros::Publisher laser_pc2_pub_;

  laser_geometry::LaserProjection laser_projector_; 
};
}
