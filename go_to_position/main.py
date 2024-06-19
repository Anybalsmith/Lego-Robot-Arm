from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait

import sys

# Create your objects here.
ev3 = EV3Brick()
motor_0 = Motor(Port.A)
motor_1 = Motor(Port.B)
motor_2 = Motor(Port.C)
motor_3 = Motor(Port.D)

# Define the positions in a dictionary
positions = {
    1: [309, 12, -170, 702],
    2: [-379, -19, -170, 702],
    3: [-1437, -37, 69, 702],
    4: [-2415, 27, -188, 702],
    5: [-3347, 23, 164, 702]
}

def move_to_position(position):
    motor_0.run_target(400, position[0], then=Stop.HOLD, wait=True)
    motor_1.run_target(400, position[1], then=Stop.HOLD, wait=True)
    motor_2.run_target(400, position[2], then=Stop.HOLD, wait=True)
    motor_3.run_target(400, position[3], then=Stop.HOLD, wait=True)

# Listen for commands from the serial port
while True:
    command = sys.stdin.readline().strip()
    if command.startswith("MOVE_TO_POSITION"):
        try:
            position_key = int(command.split()[-1])
            selected_position = positions.get(position_key)
            if selected_position:
                move_to_position(selected_position)
                print(f"Moved to position {position_key}")
            else:
                print(f"Invalid position {position_key}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Unknown command:", {command})
