import rospy
from sensor_msgs.msg import JointState

class InternalState:
  def __init__(self):
    rospy.Subscriber('stretch/joint_states', JointState, lambda data: self.set_state(data))

  def set_state(self, new_data):
    self.data = new_data

  def get_state(self):
    return self.data

if __name__ == "__main__":
  rospy.init_node("joint_state_subscriber")

  InternalState()

  rospy.spin()