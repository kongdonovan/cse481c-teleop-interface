import rospy
from control_msgs.msg import FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectoryPoint
import hello_helpers.hello_misc as hm
from std_msgs.msg import String
import time
import json
import ast

class MovePosCommand(hm.HelloNode):
  '''
  A class that sends a joint trajectory goal to stow the Stretch's arm.
  '''
  def __init__(self):
    hm.HelloNode.__init__(self)

  def issue_move_pos_command(self, pos): # moves to one pose, we want to make it work with ["raise_arm", "extend_arm", "grip", "retract_arm"]
    '''
    Function that makes an action call and sends stow position goal.
    :param self: The self reference.
    '''
    poses = json.load(open("arm_pos.json", "r"))

    stow_point = JointTrajectoryPoint()
    stow_point.time_from_start = rospy.Duration(0.000)
    position_values = poses[pos]

    # set the positions of each joint
    stow_point.positions = [position_values["arm_height"], position_values["arm_length"]]

    trajectory_goal = FollowJointTrajectoryGoal()
    # set the joints we actually want
    trajectory_goal.trajectory.joint_names = ['joint_lift', 'wrist_extension']
    trajectory_goal.trajectory.points = [stow_point]
    trajectory_goal.trajectory.header.stamp = rospy.Time(0.0)
    trajectory_goal.trajectory.header.frame_id = 'base_link'

    # if position_values["gripper"] == True:
    #   # then do a little extra to grip
    #   pass

    self.trajectory_client.send_goal(trajectory_goal)
    rospy.loginfo('Sent goal = {0}'.format(trajectory_goal))
    self.trajectory_client.wait_for_result()

  def release_gripper(self):
    # release the gripper until effort is 0.0
    pass

  def grip_gripper(self):
    # grip the gripper until a certain effort threshold
    pass

  def do_stuff(self, poses):
    for pose in ast.literal_eval(poses.data):
      self.issue_move_pos_command(pose)
    pub = rospy.Publisher('arm_pose_topic_done', String, queue_size=10)
    pub.publish("done!")

  def main(self):
    '''
    Function that initiates move_pos_command function.
    :param self: The self reference.
    '''
    hm.HelloNode.main(self, 'move_pos_command', 'move_pos_command', wait_for_first_pointcloud=False)
    rospy.Subscriber('arm_pose_topic', String, self.do_stuff) # array of poses
    rospy.loginfo('moving...')
    
    
    time.sleep(2)


if __name__ == '__main__':
  try:
    node = MovePosCommand()
    node.main()
    rospy.spin()
  except KeyboardInterrupt:
    rospy.loginfo('interrupt received, so shutting down')