import tf2_listener
import rospy
import json

rospy.init_node("tf2_listener", anonymous=True) # initialize a ros node in order to subscribe to stuff properly

listener = tf2_listener.FrameListener()

arm_height_pose = listener.get_pos()

arm_extend_pose = listener.get_pos_extend()

# grip = listener.get_grip() # we might not use this, instead decide whether it's gripping based on effort

# arm_array = arm_height_pose.split('\n')

# arm_height = arm_array[3]

arm_height = arm_height_pose.translation.z or 1

arm_extend = arm_extend_pose.translation.y or 2

def save_pos(position_name, headers, values, save_file):
    try:
        file = open(save_file, "r")
        poses = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        poses = {}
    
    poses[position_name] = {}
    # for i in range(len(headers)):
    #     poses[position_name][headers[i]] = values[i]
    poses[position_name]["arm_height"] = (-0.96327442199873 * (arm_height * 10000)) + 0.84537076355
    poses[position_name]["arm_length"] = (-0.98428984945135 * arm_extend) - 0.275424259395
    

    open(save_file, "w").write(json.dumps(poses, indent=4))



# TODO: Remove these lines below
print("Position name: ")
position_name = input()
print("Save file: ")
save_file = input()
save_pos(position_name, ["arm_height", "arm_length"], [arm_height, arm_extend], save_file)