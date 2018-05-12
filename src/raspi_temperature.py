#!/usr/bin/env python
'''raspi_temperature ROS Node'''
# license removed for brevity
import os
import rospy
from sensor_msgs.msg import Temperature

def talker():
    '''raspi_temperature Publisher'''
    pub = rospy.Publisher('raspi_temperature', Temperature, queue_size=10)
    rospy.init_node('raspi_temperature', anonymous=True)
    rate = rospy.Rate(1) # 1hz
    while not rospy.is_shutdown():
        temp = os.popen("vcgencmd measure_temp").readline()
        temp = temp.replace("temp=","")
        temp = temp[:-3]
        temperature = Temperature()
        temperature.header.stamp = rospy.Time.now()
        temperature.header.frame_id = 'base_link'
        temperature.temperature = float(temp)
        temperature.variance = 0
        pub.publish(temperature)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

