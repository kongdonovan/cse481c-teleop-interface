import rospy
from std_msgs.msg import String

class GetMedicine:
    def __init__(self):
        self.node = rospy.init_node("get_medicine") # initializes the node
        self.pub = rospy.Publisher('navigation', String, queue_size=10) # initialize the publisher

        rospy.spin()

    def sendMessage(self, message):
        self.pub.publish(message)

