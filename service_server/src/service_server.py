#! /usr/bin/env python3

import rospy
from std_srvs.srv import *

def serviceCallback(_request):

    rospy.loginfo("request : %s"%(_request.data))

    _success = True
    _message = "good"

    return SetBoolResponse(_success, _message)

def serverTest():
    rospy.init_node('service_server', anonymous=False)

    rospy.loginfo("Service Server On...")
    rospy.sleep(0.5)
    rospy.loginfo("Wait for Service Request...")

    _s = rospy.Service('/service_test', SetBool, serviceCallback)

    rospy.spin()

if __name__ == '__main__':
    try:
        serverTest()
    except rospy.ROSInternalException:
        pass
