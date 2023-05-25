from flask import Flask
app = Flask(__name__)


import stretch_body.robot

robot=stretch_body.robot.Robot()

robot.startup()

@app.route('/extend_arm')
def extend_arm():
    robot.arm.move_by(0.1)
    robot.push_command()
    return "mah"

@app.route('/retract_arm')
def retract_arm():
    robot.arm.move_by(-0.1)
    robot.push_command()
    return "mah"

@app.route('/move_forward')
def move_forward():
    robot.base.translate_by(0.25)
    robot.push_command()
    return "mah"

@app.route('/move_backwards')
def move_backwards():
    robot.base.translate_by(-0.25)
    robot.push_command()
    return "mah"

@app.route('/turn_right')
def turn_right():
    robot.base.rotate_by(-0.4)
    robot.push_command()
    return "mah"

@app.route('/turn_left')
def turn_left():
    robot.base.rotate_by(0.4)
    robot.push_command()
    return "mah"

@app.route('/startup')
def startup():
    robot.startup()
    return "mah"

@app.route('/shutdown')
def shutdown():
    robot.stop()
    return "mah"

@app.route('/move_arm_up')
def move_arm_up():
    print(robot.params)
    robot.lift.move_by(0.1)
    robot.push_command()
    return "mah"

@app.route('/release_grip')
def release_grip():
    robot.end_of_arm.move_by("stretch_gripper", 50)
    robot.push_command()
    return "mah"

@app.route('/grip')
def grip():
    robot.end_of_arm.move_by("stretch_gripper", -50)
    robot.push_command()
    return "mah"

@app.route('/move_arm_down')
def move_arm_down():
    robot.lift.move_by(-0.1)
    robot.push_command()
    return "mah"

if __name__ == '__main__':
    app.run(host="172.28.7.121")