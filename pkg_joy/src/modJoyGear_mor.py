#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import sys
import os
from morai_msgs.msg import CtrlCmd, CollisionData, EgoVehicleStatus, EventInfo, GhostMessage
from morai_msgs.srv import MoraiEventCmdSrv, MoraiEventCmdSrvResponse
from enum import Enum
from sensor_msgs.msg import Joy

class Gear(Enum):
    P = 1
    R = 2
    N = 3
    D = 4


class Trans_gear():
    def __init__(self):
        rospy.init_node("gear",anonymous=False)
        _joySub = "/joystick/joy"
        _vehStateSub = "/Ego_topic"
        _moraiEventCmdSrv = "/Service_MoraiEventCmd"
        # subscriber
        joy_sub = rospy.Subscriber(_joySub, Joy, self.joy_callback)
        Ego_status_sub = rospy.Subscriber(_vehStateSub, EgoVehicleStatus, self.ego_callback)

        # service
        rospy.wait_for_service(_moraiEventCmdSrv)
        self.event_cmd_srv = rospy.ServiceProxy(_moraiEventCmdSrv, MoraiEventCmdSrv)


        self.rate = rospy.Rate(10)
        self.request_gear = MoraiEventCmdSrvResponse()

        self.send_gear_cmd(Gear.P.value)  
        
        self.P = 0
        self.R = 0
        self.N = 0
        self.D = 0
        self.ego_status = EgoVehicleStatus()

        while not rospy.is_shutdown():
            if ( abs(self.ego_status.velocity.x) < 0.1):
                try :
                    self.gear_transfer()
                except:          
                    print('---- Down Speed ----')

            
    # Joystick_buttons to Gear
    def joy_callback(self, data):
        self.P = data.buttons[0]
        self.R = data.buttons[1]
        self.N = data.buttons[2]
        self.D = data.buttons[3]
        


    # EGO 차량 상태 정보 콜백 함수
    def ego_callback(self, data):
        self.ego_status = data
 

    # 기어 변경 이벤트 메시지 세팅 함수
    def send_gear_cmd(self, gear_mode):
        self.gear_cmd = EventInfo()
        self.gear_cmd.option = 3
        self.gear_cmd.ctrl_mode = 3
        self.gear_cmd.gear = gear_mode
        self.gear_cmd_resp = self.event_cmd_srv(self.gear_cmd)                
        # rospy.loginfo(self.gear_cmd)

    def gear_transfer(self):
    # P_Gear         
      
        if(self.P == True):
            self.send_gear_cmd(Gear.P.value)
            
            print("Gear : P")
        
        # R_Gear
        elif(self.R == True):
            self.send_gear_cmd(Gear.R.value)
            print("Gear : R")
                    
        # N_Gear
        elif(self.N == True):
            self.send_gear_cmd(Gear.N.value)
            print("Gear : N")   
             
        # D_Gear
        elif(self.D == True):
            self.send_gear_cmd(Gear.D.value)
            print("Gear : D")
                
        # print(self.gear_cmd.gear)
        
def main(args):

    gear_tranfer = Trans_gear()
    
    rospy.spin()

    # ctrl_cmd 메시지 세팅 함수


if __name__ == '__main__':
    main(sys.argv)