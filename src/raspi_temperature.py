#!/usr/bin/env python
'''raspi_temperature ROS Node'''
import os
import rospy
import tf
from sensor_msgs.msg import Temperature

def talker():
    '''raspi_temperature Publisher'''
    pub = rospy.Publisher('raspi_temperature', Temperature, queue_size=10)
    rospy.init_node('raspi_temperature', anonymous=True)
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(1)  # 1hz
    while not rospy.is_shutdown():
        br.sendTransform((-0.05, 0.0, 0.10),
                         (0.0, 0.0, 0.0, 1.0),
                         rospy.Time.now(), "raspberrypi", "base_link")
        temp = os.popen("vcgencmd measure_temp").readline()
        temp = temp.replace("temp=", "")
        temp = temp[:-3]
        temperature = Temperature()
        temperature.header.stamp = rospy.Time.now()
        temperature.header.frame_id = 'raspberrypi'
        temperature.temperature = float(temp)
        temperature.variance = 0
        pub.publish(temperature)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
