#include "laserscan_to_pointcloud/laserscan_to_pointcloud.h"

namespace laserscan_to_pointcloud
{

using namespace Eigen;
using namespace std;

LaserscanToPointcloud::LaserscanToPointcloud(const ros::NodeHandle & nh, const ros::NodeHandle & pnh) 
: nh_(nh)
, pnh_(pnh)
{
    laser_scan_sub_ = nh_.subscribe("/scan", 1, &LaserscanToPointcloud::lidarCallback, this, ros::TransportHints().tcpNoDelay());

    laser_pc2_pub_ = nh_.advertise<sensor_msgs::PointCloud2>("/velodyne_points",1);
}

LaserscanToPointcloud::~LaserscanToPointcloud()
{
}

void LaserscanToPointcloud::lidarCallback(const sensor_msgs::LaserScan::ConstPtr &msg)
{
   sensor_msgs::PointCloud2 pc2;
   laser_projector_.projectLaser(*msg, pc2);
   laser_pc2_pub_.publish(pc2);
}

} // namespace 
