# File used for setting arm pose of stretch robot

import rospy
from control_msgs.msg import FollowJointTrajectoryGoal
from std_msgs.msg import String
from trajectory_msgs.msg import JointTrajectoryPoint
import hello_helpers.hello_misc as hm
import time
import json

class MovePosCommand(hm.HelloNode):
  '''
  A class that sends a joint trajectory goal to stow the Stretch's arm.
  '''
  def __init__(self):
    hm.HelloNode.__init__(self)

  def issue_move_pos_command(self, pos):
    '''
    Function that makes an action call and sends stow position goal.
    :param self: The self reference.
    '''
    poses = json.load(open("arm_pos.json", "r"))

    stow_point = JointTrajectoryPoint()
    stow_point.time_from_start = rospy.Duration(0.000)
    position_values = poses[pos]

    stow_point.positions = [position_values["arm_height"], position_values["arm_length"]]

    trajectory_goal = FollowJointTrajectoryGoal()
    trajectory_goal.trajectory.joint_names = ['joint_lift', 'wrist_extension']
    trajectory_goal.trajectory.points = [stow_point]
    trajectory_goal.trajectory.header.stamp = rospy.Time(0.0)
    trajectory_goal.trajectory.header.frame_id = 'base_link'

    self.trajectory_client.send_goal(trajectory_goal)
    rospy.loginfo('Sent goal = {0}'.format(trajectory_goal))
    self.trajectory_client.wait_for_result()

  def main(self):
    '''
    Function that initiates move_pos_command function.
    :param self: The self reference.
    '''
    hm.HelloNode.main(self, 'move_pos_command', 'move_pos_command', wait_for_first_pointcloud=False)
    rospy.loginfo('moving...')
    # print("Select a pose:")
    # pose_name = input()
    node = rospy.init_node("goto_pose")
    rospy.Subscriber("get_medicine", String, self.issue_move_pos_command)
    rospy.spin()


if __name__ == '__main__':
  try:
    node = MovePosCommand()
    node.main()
  except KeyboardInterrupt:
    rospy.loginfo('interrupt received, so shutting down')