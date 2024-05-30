#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
ports = [Port.A, Port.B, Port.C, Port.D]
names = ["Plateforme", "Bras (bas)", "Bras (haut)", "Pince"]
motors = [None, None, None, None]
angles = [0, 0, 0, 0]  # Stocke les angles des moteurs
port_names = ["A", "B", "C", "D"]
m1 = Motor(Port.A)
m2 = Motor(Port.B)
prev_motor = None
motor_platform = Motor(Port.A)
Ze = 12 # number of teeth drive wheel
Zs = 140 # number of teeth driven wheel
output_angle = 180

# Print plateform motor position

def print_motor_position():
    current_angle = motor_platform.angle()
    ev3.screen.clear()
    ev3.screen.print('Angle actuel:')
    ev3.screen.print(current_angle)
    print('Angle actuel:', current_angle)

# Plateform initialisation
ev3.screen.clear()
# print_motor_position()
# wait(200)
ev3.screen.print('Démarrage calibration...')
print('Calibration...')
motor_platform.reset_angle(0)


def move_platform(state):
    speed = 400
    input_angle = output_angle*Zs/Ze 
    if state == 'POSITIVE':
        motor_platform.run_angle(speed, input_angle, Stop.HOLD, True)
    elif state == 'NEGATIVE':
        motor_platform.run_angle(speed, -input_angle, Stop.HOLD, True)
    elif state == 'NEUTRAL':
        motor_platform.hold()

# Rotate plateform
states = ['POSITIVE', 'NEUTRAL', 'NEGATIVE', 'NEUTRAL']
move_platform('POSITIVE')
print_motor_position()
# for state in states:
#     move_platform(state)
#     ev3.screen.print(state)
#     print_motor_position()
#     print(state)
    