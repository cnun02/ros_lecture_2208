#!/usr/bin/env python3
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import rospy

class Joystick: 
    def __init__(self):
        super(Joystick, self).__init__()

        _joySub = "/joystick/joy"
        _joyPub = "/cmd_vel"
        # subscriber
        self.joy_sub = rospy.Subscriber(_joySub, Joy, self.callbackJoy)
        # publisher
        self.con_pub = rospy.Publisher(_joyPub, Twist, queue_size = 1)
        
        self.rate = rospy.Rate(10)
        
        self.horizon = 0
        self.vertical = 0

        self.vertical_accel = 0
        self.horizon_steer = 0

        self.main()

    # joystick
    def callbackJoy(self, data):
        self.vertical_accel = data.axes[7] 
        self.horizon_steer = data.axes[3]
        
    def main(self):

        _ctrl_msg = Twist()

        while not rospy.is_shutdown():

            _ctrl_msg.linear.x = self.vertical_accel * 0.3
            _ctrl_msg.angular.z = self.horizon_steer * 0.5

            self.con_pub.publish(_ctrl_msg)
            
            self.rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('joy_xbox', anonymous= False)

        _joystick1 = Joystick()
        
        rospy.spin()

    except rospy.ROSInterruptException:
        pass