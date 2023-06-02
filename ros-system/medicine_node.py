import rospy
from std_msgs.msg import String

class GetMedicine:
    def __init__(self):
        self.pub = rospy.Publisher('meds_topic', String, queue_size=10) # initialize the publisher

    def sendMessage(self, message):
        print(message)
        self.pub.publish(message)

if __name__ == '__main__':
    
    # Initialize the node, and call it "tf2_liistener"
    rospy.init_node('get_medicine')

    # Instantiate the `FrameListener()` class
    GetMedicine()

    # Give control to ROS.  This will allow the callback to be called whenever new
    # messages come in.  If we don't put this line in, then the node will not work,
    # and ROS will not process any messages
    rospy.spin()