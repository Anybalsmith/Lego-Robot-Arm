#!/usr/bin/env pybricks-micropython

from pybricks.messaging import BluetoothMailboxServer, TextMailbox
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop

ev3 = EV3Brick()
server = BluetoothMailboxServer()
mbox = TextMailbox('greeting', server)

motor_platform = Motor(Port.A)
motor_arm_1 = Motor(Port.B)
motor_arm_2 = Motor(Port.C)
motor_gripper = Motor(Port.D)


# Zustände der Sensoren
NEGATIVE = 0
NEUTRAL = 1
POSITIVE = 2

prev_x_state = NEUTRAL
prev_y_state = NEUTRAL
prev_button_state = NEGATIVE 


# Kalibrierung Motoren
ev3.screen.clear()
ev3.screen.print('Starte Kalibrierung...')
print('Kalibrierung...')
motor_platform.reset_angle(0)
motor_arm_1.reset_angle(0)
motor_arm_2.reset_angle(0)
motor_gripper.reset_angle(0)


# Verbindung zum Client
print('Warte auf Verbindung...')
ev3.screen.clear()
ev3.screen.print('Warte auf Verbindung...')
server.wait_for_connection()
print('Verbunden!')
ev3.screen.clear()
ev3.screen.print('Verbunden!')


# Funktion zum Steuern des Arms
def move_arm(state):
    speed_motor_1 = 200
    speed_motor_2 = -170
    if state == 'POSITIVE':
        if motor_arm_1.angle() < 900:
            motor_arm_1.run_target(speed_motor_1, 900, then=Stop.HOLD, wait=False)
        elif motor_arm_1.angle() >= 900 and motor_arm_2.angle() > -700:
            motor_arm_1.run_target(speed_motor_1, 1640, then=Stop.HOLD, wait=False)
            motor_arm_2.run_target(speed_motor_2, -700, then=Stop.HOLD, wait=False)
        elif motor_arm_1.angle() >= 1640 or motor_arm_2.angle() <= -700:
            motor_arm_1.hold() 
            motor_arm_2.hold()

    if state == 'NEGATIVE':
        if motor_arm_1.angle() < 900:
            motor_arm_1.run_target(-speed_motor_1, 0, then=Stop.HOLD, wait=False)
        elif motor_arm_1.angle() >= 900 and motor_arm_2.angle() < 0:
            motor_arm_1.run_target(-speed_motor_1, 900, then=Stop.HOLD, wait=False)
            motor_arm_2.run_target(-speed_motor_2, 0, then=Stop.HOLD, wait=False)    
        elif motor_arm_1.angle() <= 0 or motor_arm_2.angle() >= 0:
            motor_arm_1.hold() 
            motor_arm_2.hold()

    if state == 'NEUTRAL':
        motor_arm_1.hold()
        motor_arm_2.hold()


def move_platform(state):
    speed = 400
    if state == 'POSITIVE':
        motor_platform.run(-speed)
    elif state == 'NEGATIVE':
        motor_platform.run(speed)
    elif state == 'NEUTRAL':
        motor_platform.hold()


def move_gripper(state):
    speed = -200
    if state == 'PRESSED':
        if(motor_gripper.angle() >= -320):
            motor_gripper.run_target(speed, -320, then=Stop.HOLD, wait=False)
        else:
            motor_gripper.hold()
    elif state == 'RELEASED':
        if(motor_gripper.angle() <= 0):
            motor_gripper.run_target(-speed, 0, then=Stop.HOLD, wait=False)
        else:
            motor_gripper.hold()



while True:
    mbox.wait() 
    message = mbox.read().split('-')
    print("Nachricht: "+str(message))
    sensor = message[0]
    state = message[1]
    
    if sensor == 'X':
        move_platform(state)           
    elif sensor == 'Y':
        move_arm(state)        
    elif sensor == 'BUTTON':
        move_gripper(state)


        

       

