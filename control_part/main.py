#!/usr/bin/env pybricks-micropython

import math
import time
from ikine import ikine
# from grab import grab
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop
#from pybricks.messaging import BluetoothMailboxServer, TextMailbox

# Initialisation des composants EV3
ev3 = EV3Brick()
#server = BluetoothMailboxServer()
#mbox = TextMailbox('greeting', server)

motor_platform = Motor(Port.A)
motor_arm_1 = Motor(Port.B)
motor_arm_2 = Motor(Port.C)
motor_gripper = Motor(Port.D)


# Position initiale (en radians)
initial_q1 = 0.0
initial_q2 = 0.0
initial_q3 = 0.0

# Position courante du robot
current_q1 = initial_q1
current_q2 = initial_q2
current_q3 = initial_q3

# Fonction pour convertir les angles en degrés et prise en compte des rapports de réduction
def to_degrees(q1, q2, q3):
    q1 = math.degrees(q1)
    q2 = math.degrees(q2)
    q3 = math.degrees(q3)

    # conversion q1
    Ze_plateform = 12 # number of teeth drive wheel
    Zs_plateform = 140 # number of teeth driven wheel
    q1 = q1*Zs_plateform/Ze_plateform

    # conversion q2
    Z1_b1 = 12
    Z2_b1 = 36
    Z3_b1 = 12
    Z4_b1 = 36
    q2 = q2*Z2_b1*Z4_b1/(Z1_b1*Z3_b1)

    # conversion q3
    Z1_b2 = 12
    Z2_b2 = 20
    Z3_b2 = 12
    Z4_b2 = 36
    q3 = q3*Z2_b2*Z4_b2/(Z1_b2*Z3_b2)
    return q1, q2, q3



# Fonction pour déplacer le bras à une position donnée (x, y, z)
def move_to(x, y, z):
    try:
        # Calcul des angles à partir des coordonnées (x, y, z)
        q1, q2, q3 = ikine(x, y, z)

        # Convertir les angles en degrés
        q1_deg, q2_deg, q3_deg = to_degrees(q1, q2, q3)
        
        # Déplacer les moteurs aux angles calculés
        motor_platform.run_target(200, q1_deg, then=Stop.HOLD, wait=False)
        motor_arm_1.run_target(200, q2_deg, then=Stop.HOLD, wait=False)
        motor_arm_2.run_target(200, q3_deg, then=Stop.HOLD, wait=True)  # wait=True to ensure arm 2 movement completes before next action

        # Mettre à jour la position courante
        current_q1 = q1
        current_q2 = q2
        current_q3 = q3

        #print(f'Moved to ({x}, {y}, {z}): q1={q1_deg}, q2={q2_deg}, q3={q3_deg}')
    except ValueError as e:
        print("Position impossible à atteindre:", e)
    return q1_deg, q2_deg, q3_deg

# Initialisation du robot
def initialize_robot():
    global current_q1, current_q2, current_q3
    print('Initialisation du robot...')
    motor_platform.reset_angle(0)
    motor_arm_1.reset_angle(0)
    motor_arm_2.reset_angle(0)
    motor_gripper.reset_angle(0)
    
    # Déplacer le robot à sa position initiale
    q1_deg, q2_deg, q3_deg = to_degrees(initial_q1, initial_q2, initial_q3)
    motor_platform.run_target(200, q1_deg, then=Stop.HOLD, wait=False)
    motor_arm_1.run_target(200, q2_deg, then=Stop.HOLD, wait=False)
    motor_arm_2.run_target(200, q3_deg, then=Stop.HOLD, wait=True)

    current_q1 = initial_q1
    current_q2 = initial_q2
    current_q3 = initial_q3

    print('Robot initialisé à sa position de départ')

# Calibration des moteurs et initialisation
ev3.screen.clear()
ev3.screen.print('Démarrage calibration...')
print('Calibration...')
print(motor_platform.angle())
print(motor_arm_1.angle())
print(motor_arm_2.angle())
time.sleep(2)
#initialize_robot()


# Exemple d'utilisation : Déplacer le robot à plusieurs positions successives
move_to(0, 0, 0.001)
print("mvt 1 done")
time.sleep(5)










# q1, q2, q3 = ikine(0.12, 0.12, -0.05)
# print('ikine',q1, q2, q3)
# q1_deg, q2_deg, q3_deg = to_degrees(q1, q2, q3)
# print(q1_deg, q2_deg, q3_deg)
# Z1_b2 = 12
# Z2_b2 = 20
# Z3_b2 = 12
# Z4_b2 = 36
# motor_arm_2.run_target(200, 45*Z2_b2*Z4_b2/(Z1_b2*Z3_b2), then=Stop.HOLD, wait=False)
# Z1_b1 = 12
# Z2_b1 = 36
# Z3_b1 = 12
# Z4_b1 = 36
# motor_arm_1.run_target(200, 45*Z2_b1*Z4_b1/(Z1_b1*Z3_b1), then=Stop.HOLD, wait=False)
#motor_arm_1.run_target(200, q2_deg, then=Stop.HOLD, wait=False)
#motor_arm_2.run_target(200, q3_deg, then=Stop.HOLD, wait=True)  # wait=True to ensure arm 2 movement completes before next action
# q1_deg, q2_deg, q3_deg = move_to(0.12, 0.12, -0.05)
# print("mvt 2 done")
# print(q1_deg, q2_deg, q3_deg)
# time.sleep(5)
# move_to(50, 150, 100)
# print("mvt 3 done")
# move_to(0, 200, 100)
# print("mvt 4 done")

# grab()
# print('grab_done')
