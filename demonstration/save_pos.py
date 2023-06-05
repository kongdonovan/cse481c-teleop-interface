import tf2_listener
import rospy
import json
import internal_state

rospy.init_node("tf2_listener", anonymous=True) # initialize a ros node in order to subscribe to stuff properly

listener = tf2_listener.FrameListener()

grip_pose = internal_state.InternalState()

arm_height_pose = grip_pose.get_state().position[2]

arm_extend_pose = grip_pose.get_state().position[10]

is_gripped = grip_pose.get_state().effort[5] < -6

# grip = listener.get_grip() # we might not use this, instead decide whether it's gripping based on effort

# arm_array = arm_height_pose.split('\n')

# arm_height = arm_array[3]

arm_height = arm_height_pose

arm_extend = arm_extend_pose

def save_pos(position_name, headers, values, save_file):
    try:
        file = open(save_file, "r")
        poses = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        poses = {}
    
    poses[position_name] = {}
    # for i in range(len(headers)):
    #     poses[position_name][headers[i]] = values[i]

    # save the arm height and arm length
    poses[position_name]["arm_height"] = arm_height
    poses[position_name]["arm_length"] = arm_extend
    poses[position_name]["is_gripped"] = is_gripped
    

    open(save_file, "w").write(json.dumps(poses, indent=4))



# TODO: Remove these lines below
print("Position name: ")
position_name = input()
print("Save file: ")
save_file = input()
save_pos(position_name, ["arm_height", "arm_length"], [arm_height, arm_extend], save_file)