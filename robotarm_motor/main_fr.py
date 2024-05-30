#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Button
from pybricks.ev3devices import Motor
import utime

ev3 = EV3Brick()
current_port_index = 0
ports = [Port.A, Port.B, Port.C, Port.D]
names = ["Plateforme", "Bras (bas)", "Bras (haut)", "Pince"]
motors = [None, None, None, None]
angles = [0, 0, 0, 0]  # Stocke les angles des moteurs
port_names = ["A", "B", "C", "D"]
m1 = Motor(Port.A)
m2 = Motor(Port.B)
prev_motor = None

def get_motor(port_index):
    if motors[port_index] is None:
        try:
            motors[port_index] = Motor(ports[port_index])
            # Optionnel : Réinitialise l'angle du moteur à 0 lors de l'initialisation
            motors[port_index].reset_angle(0)
        except:
            pass  # Si le moteur n'est pas connecté, une exception est capturée.
    return motors[port_index]

current_motor = get_motor(current_port_index)

def switchState_and_print(new_motor):
    global prev_motor
    
    if new_motor != prev_motor:
        ev3.screen.clear()
        ev3.screen.print("Port: " + str(port_names[current_port_index]) +"\n"+ names[current_port_index])
        prev_motor = new_motor

wasPressed = False
current_motor = get_motor(current_port_index)
ev3.screen.clear()
ev3.screen.print("Port: " + str(current_port_index) +"\n"+ names[current_port_index])

while True:
    if Button.CENTER in ev3.buttons.pressed():
        if not wasPressed:  
            print("Angles de tous les moteurs :") 
            for index, motor in enumerate(motors):
                if motor:
                    angles[index] = motor.angle()  # Stocke l'angle du moteur
                    print(names[index] + ": " + str(angles[index]))
            wasPressed = True
    else:
        wasPressed = False

    # Si le bouton est pressé, démarre la rotation
    if Button.LEFT in ev3.buttons.pressed():
        current_motor.run(360)  

    elif Button.RIGHT in ev3.buttons.pressed():
        current_motor.run(-360)  

    else:
        # Si aucun bouton n'est pressé, le moteur s'arrête
        current_motor.hold()

    # Vérifie si les boutons sont pressés pour changer le port actuel
    if Button.DOWN in ev3.buttons.pressed():
        current_port_index = (current_port_index + 1) % 4
        current_motor = get_motor(current_port_index)
        switchState_and_print(current_motor)
        utime.sleep(1)

    elif Button.UP in ev3.buttons.pressed():
        current_port_index = (current_port_index - 1) % 4
        current_motor = get_motor(current_port_index)
        switchState_and_print(current_motor)
        utime.sleep(1)
