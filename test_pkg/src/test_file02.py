#! /usr/bin/env python3

import rospy as rp # ros python module 참조
from std_msgs.msg import * # 사전 정의된 ros standard message의 모든 타입 참조
from test_pkg.msg import myMsg

class test(): # python class 선언
    def __init__(self): # 초기화 함수 정의
        super(test, self).__init__() # class 초기화

        self.rate = rp.Rate(10) # 10hz

        self.publisher = rp.Publisher('/topic_name', Int8, queue_size=10) # ros publisher 생성

        self.main()

    def main(self): # class main 함수 정의
        _n = 0 # 지역변수 _n 정의 및 초기화

        _testMsg = myMsg()

        while not rp.is_shutdown(): # ros가 종료되기 전까지 계속 반복
             
             _n = _n + 1 # _n을 1씩 증가시킴

             _testMsg.count = _n
             _testMsg.data = 123.123
             _testMsg.status = "hello ROS"

             self.publisher.publish(_testMsg) # Publish 실행

             self.rate.sleep() # while loop를 10hz로 동작시킨다

if __name__ == '__main__': # 본 바일이 메인 실행파일일때
    rp.init_node("test_node", anonymous=False) # ros node 정의 및 초기화
    _run = test() # test class 생성(호출)
    rp.spin() # ros node 유지
