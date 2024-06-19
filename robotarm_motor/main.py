#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Button
from pybricks.ev3devices import Motor
import utime

ev3 = EV3Brick()
current_port_index = 0
ports = [Port.A, Port.B, Port.C, Port.D]
names = ["Plattform", "Arm (unten)", "Arm (oben)", "Zange"]
motors = [None, None, None, None]
angles = [0, 0, 0, 0]  # Speichert die Winkel der Motoren
port_names = ["A", "B", "C", "D"]
m1 = Motor(Port.A)
m2 = Motor(Port.B)
prev_motor = None

def get_motor(port_index):
    if motors[port_index] is None:
        try:
            motors[port_index] = Motor(ports[port_index])
            # Optional: Setzt den Winkel des Motors auf 0 bei Initialisierung
            motors[port_index].reset_angle(0)
        except:
            pass  # Falls der Motor nicht angeschlossen ist, wird eine Exception gefangen.
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
            print("Winkel aller Motoren:") 
            for index, motor in enumerate(motors):
                if motor:
                    angles[index] = motor.angle()  # Speichert den Winkel des Motors
                    print(names[index] + ": " + str(angles[index]))
            wasPressed = True
    else:
        wasPressed = False


    # Wenn der Knopf gedrückt wird, startet die Drehung
    if Button.LEFT in ev3.buttons.pressed():
        current_motor.run(360)
        print(current_port_index)
        print(current_motor.angle())  

    elif Button.RIGHT in ev3.buttons.pressed():
        current_motor.run(-360)
        print(current_port_index)
        print(current_motor.angle())  

    else:
        # Wenn keine der Tasten gedrückt wird, stoppt der Motor
        current_motor.hold()

    # Überprüfen, ob die Tasten gedrückt werden, um den aktuellen Port zu ändern
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

        


