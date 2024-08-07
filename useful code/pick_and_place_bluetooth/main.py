#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait
from pybricks.messaging import BluetoothMailboxClient, TextMailbox

import time


ev3 = EV3Brick()
client = BluetoothMailboxClient()
mbox = TextMailbox('command', client)


server_address = 'A5:69:94:A4:AA:01'

motor_platform = Motor(Port.A)
motor_arm_1 = Motor(Port.B)
motor_arm_2 = Motor(Port.C)
motor_gripper = Motor(Port.D)

# Define the positions in a dictionary
positions = {
    0: [0, 0, 0, 0, 0],
    1: [309, 12, -170, 702],
    2: [-379, -19, -170, 702],
    3: [-1437, -37, 69, 702],
    4: [-2415, 27, -188, 702],
    5: [-3347, 23, 164, 702]
}

def move_to_position(position):
    motor_platform.run_target(400, position[0], then=Stop.HOLD, wait=True)
    motor_arm_2.run_target(400, position[2], then=Stop.HOLD, wait=True)
    motor_arm_1.run_target(400, position[1], then=Stop.HOLD, wait=True)
    motor_gripper.run_target(400, position[3], then=Stop.HOLD, wait=True)

def initialisation_arm():
    motor_platform.run_target(400, 0, then=Stop.HOLD, wait=True)
    motor_arm_1.run_target(400, -250, then=Stop.HOLD, wait=True)
    motor_arm_2.run_target(400, 0, then=Stop.HOLD, wait=True)
    motor_gripper.run_target(400,1000, then=Stop.HOLD, wait=True)

def pick(position):
    move_to_position(positions[position])
    # pick
    motor_gripper.run_target(400,350, then=Stop.HOLD, wait=True)
    time.sleep(2)
    motor_arm_1.run_target(400, -137, then=Stop.HOLD, wait=True)
    time.sleep(2)

def place(position):
    motor_arm_1.run_target(400, -350, then=Stop.HOLD, wait=True)
    # Move to the place position
    motor_platform.run_target(400, positions[position][0], then=Stop.HOLD, wait=True)
    motor_arm_2.run_target(400, -250, then=Stop.HOLD, wait=True)
    # Place action
    motor_gripper.run_target(400, 702, then=Stop.HOLD, wait=True)
    time.sleep(2)

def reset_pose():
    # go to initial position
    motor_platform.run_target(400, 0, then=Stop.HOLD, wait=True)
    motor_arm_1.run_target(400, 0, then=Stop.HOLD, wait=True)
    motor_arm_2.run_target(400, 0, then=Stop.HOLD, wait=True)
    motor_gripper.run_target(400,0, then=Stop.HOLD, wait=True)

print('Connecting...')
ev3.screen.clear()
ev3.screen.print('Connecting...')
client.connect(server_address)
print('Connected!')
ev3.screen.clear()
ev3.screen.print('Connected!')

mbox.send('sex')


while True:
    command = mbox.read()
    while command is None:
        print("Waiting for command...")
        ev3.screen.clear()
        ev3.screen.print('Waiting for command...')
        command = mbox.read()
        time.sleep(1)  

    command = command.strip()
    if command.startswith("pick") and "place" in command:
        try:
            parts = command.split()
            initialisation_arm()
            pick_position = int(parts[1])
            place_position = int(parts[3])
            pick(pick_position)
            place(place_position)
            print("Picked from position", pick_position, "and placed at position", place_position)
            reset_pose()
            print("Reset pose done")
            # Answer to the server
            mbox.send("Operation completed")
        except Exception as e:
            print("Error:", e)
            mbox.send("Error:", e)
    else:
        print("Unknown command:", command)
        mbox.send("Unknown command")
