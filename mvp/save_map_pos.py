import tf2_map_listener
import rospy
import json

rospy.init_node("map_listener", anonymous=True) # initialize a ros node in order to subscribe to stuff properly

listener = tf2_map_listener.MapListener()

map_pos = listener.get_map_pos()

print(map_pos)

# grip = listener.get_grip() # we might not use this, instead decide whether it's gripping based on effort

# arm_array = arm_height_pose.split('\n')

# arm_height = arm_array[3]

def save_pos(position_name, headers, values, save_file):
    try:
        file = open(save_file, "r")
        poses = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        poses = {}

    poses[position_name] = {}
    for i in range(len(headers)):
        poses[position_name][headers[i]] = values[i]

    open(save_file, "w").write(json.dumps(poses, indent=4))



# TODO: Remove these lines below
print("Position name: ")
position_name = input()
print("Save file: ")
save_file = input()
save_pos(position_name, ["x", "y", "z"], [map_pos.translation.x, map_pos.translation.y, map_pos.rotation.z], save_file)