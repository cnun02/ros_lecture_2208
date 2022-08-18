#! /usr/bin/env python3
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from squaternion import Quaternion

from std_msgs.msg import *
from std_srvs.srv import *
from test_pkg.msg import myMsg

import rospy as rp
import math

class test():
    def __init__(self):
        super(test, self).__init__()

        self.bJoyEnable = True
        _joySub = "/joystick/joy"
        _command_Pub = "/cmd_vel"
        _turtleOdom = "/odom"
        _turtleImu = "/imu"
        _myMsg_pub = "/mymsg_topic"

        _srv_joyEnable = "/joy_enable"

        _kp = rp.get_param("/path_following_node/kp")
        _ki = rp.get_param("/path_following_node/ki")

        self.wayPoints_x = [0, 5, 5, 0]
        self.wayPoints_y = [0, 0, 5, 5]

        self.vertical_accel = 0
        self.horizon_steer = 0

        self.turtle_pos_x = 0
        self.turtle_pos_y = 0
        self.turtle_pos_z = 0

        self.v_cmd = 0.3

        self.Threshold_dist = 1

        self.e_store = 0

        self.kp = _kp
        self.ki = _ki

        self.dt = 0.1

        self.turtle_heading_angle = 0

        self.rate = rp.Rate(10)

        self.command_pub = rp.Publisher(_command_Pub, Twist, queue_size = 1)
        self.myMsg_pub = rp.Publisher(_myMsg_pub, myMsg, queue_size=10)

        self.joy_sub = rp.Subscriber(_joySub, Joy, self.subCallBackJoy)
        self.turtleOdom_sub = rp.Subscriber(_turtleOdom, Odometry, self.subCallbackOdom)
        self.turtleImu_sub = rp.Subscriber(_turtleImu, Imu, self.subCallbackImu)
        
        self.service_server = rp.Service(_srv_joyEnable, SetBool, self.serviceCallback)

        self.main()

    def subCallbackOdom(self, _data:Odometry):
        self.turtle_pos_x = _data.pose.pose.position.x
        self.turtle_pos_y = _data.pose.pose.position.y
        self.turtle_pos_z = _data.pose.pose.position.z
    
    def subCallbackImu(self, _data:Imu):
        _quaternion_w = _data.orientation.w
        _quaternion_x = _data.orientation.x
        _quaternion_y = _data.orientation.y
        _quaternion_z = _data.orientation.z
        _quaternion = Quaternion(_quaternion_w, _quaternion_x, _quaternion_y, _quaternion_z)
        _euler_roll, _euler_pitch, _euler_yaw = _quaternion.to_euler()

        self.turtle_heading_angle = _euler_yaw

    def subCallBackJoy(self, _data):
        self.vertical_accel = _data.axes[7] 
        self.horizon_steer = _data.axes[3]

    def serviceCallback(self, _request):
        self.bJoyEnable = _request.data
        rp.loginfo("Joy_Stick_Enable : {0}".format(self.bJoyEnable))
        _temp_string = "Joy Stick Enable : {0}".format(self.bJoyEnable)

        return SetBoolResponse(self.bJoyEnable, _temp_string)
    
    def angleCheck(self, _angle):

        _output = _angle

        if abs(_angle) > math.pi:
            if _angle < 0:
                _output = _angle + 2 * math.pi
            else:
                _output = _angle - 2 * math.pi

        return _output

    def main(self):
        _ctrl_msg = Twist()
        _myMsg = myMsg()
        _wpNum = 0
        _nTemp = 0

        while not rp.is_shutdown():

            if self.bJoyEnable:
                _ctrl_msg.linear.x = self.vertical_accel * 0.3
                _ctrl_msg.angular.z = self.horizon_steer * 0.5
                self.e_store = 0
            else:
                _v_cmd = self.v_cmd

                _dist = math.sqrt(math.pow(self.wayPoints_x[_wpNum] - self.turtle_pos_x, 2) \
                                + math.pow(self.wayPoints_y[_wpNum] - self.turtle_pos_y, 2))

                if abs(_dist) < self.Threshold_dist:
                    _wpNum = _wpNum + 1
                    if _wpNum >= len(self.wayPoints_x):
                        _wpNum = 0

                _desAngle = math.atan2(self.wayPoints_y[_wpNum] - self.turtle_pos_y,\
                                  self.wayPoints_x[_wpNum] - self.turtle_pos_x)

                _desAngle = self.angleCheck(_desAngle)

                _e_angle = _desAngle - self.turtle_heading_angle

                _e_angle = self.angleCheck(_e_angle)

                _p_term = self.kp * _e_angle
                _i_term = self.ki * self.dt * self.e_store

                _angleCmd = _p_term + _i_term

                _ctrl_msg.angular.z = _angleCmd
                _ctrl_msg.linear.x = _v_cmd

                self.e_store = self.e_store + _e_angle

            _nTemp = _nTemp + 1

            _myMsg.count = _nTemp
            _myMsg.data = self.turtle_heading_angle
            _myMsg.status = "good"

            self.command_pub.publish(_ctrl_msg)
            self.myMsg_pub.publish(_myMsg)
            
            self.rate.sleep()

if __name__=='__main__':
    rp.init_node("test_node", anonymous=False)
    _run = test()
    rp.spin()