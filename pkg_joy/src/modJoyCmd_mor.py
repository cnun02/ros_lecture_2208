#!/usr/bin/env python3
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import rospy
from morai_msgs.msg import CtrlCmd, EgoVehicleStatus, EventInfo
from morai_msgs.srv import MoraiEventCmdSrv
import threading
from enum import Enum

class Joystick:
    def __init__(self):        
        rospy.init_node('ctrl_cmd', anonymous= True)
        _joySub = "/joystick/joy"
        _joyPub = "/ctrl_cmd"
        # subscriber
        self.joy_sub = rospy.Subscriber(_joySub, Joy,self.joy)
        # self.status_sub = rospy.Subscriber('EgoStatus', EgoVehicleStatus, self.ego_status)
        
        # publisher
        self.con_pub = rospy.Publisher(_joyPub,CtrlCmd, queue_size = 1)
        # self.event_cmd_srv = rospy.ServiceProxy('Service_MoraiEventCmd', MoraiEventCmdSrv)
        self.rate = rospy.Rate(10)
        
        self.horizon = 0
        self.vertical = 0
        self.minus = 0

    # joystick 설정     
    def joy(self, data):
        self.vertical = data.axes[7] 
        self.horizon = data.axes[3]
        
    def morai(self):
        
        # CmdType == 2 -> velocity CmdType == 3 -> acceleration
        ctrl_msg = CtrlCmd()
        while not rospy.is_shutdown():
            # ctrl_msg.longlCmdType = 3
            # ctrl_msg.steering = self.horizon 
            # ctrl_msg.acceleration = self.vertical * 10
            
            ctrl_msg.longlCmdType = 2
            ctrl_msg.steering = self.horizon 
            ctrl_msg.velocity = self.vertical * 40


            self.con_pub.publish(ctrl_msg)
            
            self.rate.sleep()
            
        rospy.spin()

if __name__ == '__main__':
    try:
        print('start')
        joystick1 = Joystick()
        t = threading.Thread(target = joystick1.morai(), args=())
        t.start()
    except rospy.ROSInterruptException:
        pass
