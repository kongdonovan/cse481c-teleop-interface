#!/usr/bin/env python3

import rospy
import actionlib
import sys
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Quaternion
from std_msgs.msg import String
from tf import transformations
import json

class StretchNavigation:
    """
    A simple encapsulation of the navigation stack for a Stretch robot.
    """
    def __init__(self):
        """
        Create an instance of the simple navigation interface.
        :param self: The self reference.
        """
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()
        rospy.loginfo('{0}: Made contact with move_base server'.format(self.__class__.__name__))

        self.goal = MoveBaseGoal()
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.header.stamp = rospy.Time()

        self.goal.target_pose.pose.position.x = 0.0
        self.goal.target_pose.pose.position.y = 0.0
        self.goal.target_pose.pose.position.z = 0.0
        self.goal.target_pose.pose.orientation.x = 0.0
        self.goal.target_pose.pose.orientation.y = 0.0
        self.goal.target_pose.pose.orientation.z = 0.0
        self.goal.target_pose.pose.orientation.w = 1.0

    def get_quaternion(self,theta):
        """
        A function to build Quaternians from Euler angles. Since the Stretch only
        rotates around z, we can zero out the other angles.
        :param theta: The angle (radians) the robot makes with the x-axis.
        """
        return Quaternion(*transformations.quaternion_from_euler(0.0, 0.0, theta))

    def go_to(self, x, y, theta):
        """
        Drive the robot to a particular pose on the map. The Stretch only needs
        (x, y) coordinates and a heading.
        :param x: x coordinate in the map frame.
        :param y: y coordinate in the map frame.
        :param theta: heading (angle with the x-axis in the map frame)
        """
        rospy.loginfo('{0}: Heading for ({1}, {2}) at {3} radians'.format(self.__class__.__name__,
        x, y, theta))

        self.goal.target_pose.pose.position.x = x
        self.goal.target_pose.pose.position.y = y
        self.goal.target_pose.pose.orientation = self.get_quaternion(theta)

        self.client.send_goal(self.goal, done_cb=self.done_callback)
        self.client.wait_for_result()

    def done_callback(self, status, result):
        """
        The done_callback function will be called when the joint action is complete.
        :param self: The self reference.
        :param status: status attribute from MoveBaseActionResult message.
        :param result: result attribute from MoveBaseActionResult message.
        """
        if status == actionlib.GoalStatus.SUCCEEDED:
            rospy.loginfo('{0}: SUCCEEDED in reaching the goal.'.format(self.__class__.__name__))
        else:
            rospy.loginfo('{0}: FAILED in reaching the goal.'.format(self.__class__.__name__))

# change this to send a sequence of poses
def send_base_to_move(nav, pose):
    # open the json and parse it
    file = open("positions.json", "r")
    poses = json.load(file)
    poses_to_send = None

    # access the pose we want to go to
    specific_pose = poses[pose.data]
    if specific_pose:
        # then go to that pose
        nav.go_to(specific_pose["x"], specific_pose["y"], specific_pose["z"])
        

def send_arm_to_move(back):
    poses_to_send = None
    if back:
        # this is if we are dropping off
        poses_to_send = ["raise_arm", "extend_arm", "release", "retract_arm"] # hardcoded, we can factor this out later
    else:
        # this is if we are picking up
        poses_to_send = ["release", "raise_arm", "extend_arm", "grip", "retract_arm"] # hardcoded, we can factor this out later
        
    pose_publisher = rospy.Publisher('arm_pose_topic', String, queue_size=10) # initialize the publisher
    pose_publisher.publish(str(poses_to_send)) # then publish to the right topic
    

def execute_movements(data):
    # assume the robot is at medicine. send the arm to pick up medicine
    nav = StretchNavigation() # this just allows us to move the robot
    send_arm_to_move(False) # move the arm to pick up the medicine
    rospy.wait_for_message('arm_pose_topic') # this waits for the done signal
    send_base_to_move(nav, "user") # this signifies the navigating to medicine
    send_arm_to_move(True) # this moves the arm to drop off medicine
    rospy.wait_for_message('arm_pose_topic') # this waits for the done signal
    send_base_to_move(nav, "medicine_storage") # move the base to go back to the medicine storage
    pose_publisher = rospy.Publisher('meds_done', String, queue_size=10) # initialize the publisher
    pose_publisher.publish("done!") # then publish to the right topic
    

if __name__ == '__main__':
    rospy.init_node('navigation')
    nav = StretchNavigation()

    rospy.Subscriber('meds_topic', String, execute_movements) # this tells us what medicine we want

    rospy.spin()