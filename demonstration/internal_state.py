import rospy
from sensor_msgs.msg import JointState

class InternalState:
  def __init__(self):
    self.data = None
    rospy.Subscriber('stretch/joint_states', JointState, self.set_state)
    rospy.sleep(1)

  def set_state(self, new_data):
    self.data = new_data

  def get_state(self):
    return self.data

if __name__ == "__main__":
  rospy.init_node("joint_state_subscriber")

  InternalState()

  rospy.spin()