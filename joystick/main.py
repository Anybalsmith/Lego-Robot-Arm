#!/usr/bin/env pybricks-micropython

from pybricks.messaging import BluetoothMailboxClient, TextMailbox
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Button
from pybricks.ev3devices import TouchSensor, GyroSensor
from pybricks.tools import wait, StopWatch

ev3 = EV3Brick()
SERVER = 'EV3-Robotarm'
client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)


gyro_x = GyroSensor(Port.S1)
gyro_y = GyroSensor(Port.S2)
button = TouchSensor(Port.S3)

# Sensoren-Status
NEGATIVE = 0
NEUTRAL = 1
POSITIVE = 2

prev_x_state = NEUTRAL
prev_y_state = NEUTRAL
prev_button_state = NEGATIVE 

# Kalibrierungswerte und Filterkonstanten
GYRO_CALIBRATION_LOOP_COUNT = 200
SMOOTHING_FACTOR = 0.1  # Für softwareseitige Filterung (exponentielle Glättung)
gyro_x_offset = 0
gyro_y_offset = 0
x_filtered = 0
y_filtered = 0

# Gryosensor-X Kalibrierung
def calibrateGyro_X():
    ev3.screen.clear()
    ev3.screen.print('\nKalibriere\nGyrosensor-X')
    while True:
        gyro_minimum_angle, gyro_maximum_angle = 10, -10
        gyro_x_sum = 0

        for _ in range(GYRO_CALIBRATION_LOOP_COUNT):
            gyro_sensor_value = gyro_x.angle()
            gyro_x_sum += gyro_sensor_value
            if gyro_sensor_value > gyro_maximum_angle:
                gyro_maximum_angle = gyro_sensor_value
            if gyro_sensor_value < gyro_minimum_angle:
                gyro_minimum_angle = gyro_sensor_value
            wait(5)
        if gyro_maximum_angle - gyro_minimum_angle < 0.5:
            break

    gyro_x.reset_angle(0)
    gyro_x_offset = gyro_x_sum / GYRO_CALIBRATION_LOOP_COUNT

# Gyrosensor-Y Kalibrierung
def calibrateGyro_Y():
    ev3.screen.clear()
    ev3.screen.print('\nKalibriere\nGyrosensor-Y')
    while True:
        gyro_minimum_angle, gyro_maximum_angle = 20, -20
        gyro_y_sum = 0
        for _ in range(GYRO_CALIBRATION_LOOP_COUNT):
            gyro_sensor_value = gyro_y.angle()
            gyro_y_sum += gyro_sensor_value
            if gyro_sensor_value > gyro_maximum_angle:
                gyro_maximum_angle = gyro_sensor_value
            if gyro_sensor_value < gyro_minimum_angle:
                gyro_minimum_angle = gyro_sensor_value
            wait(5)
        if gyro_maximum_angle - gyro_minimum_angle < 0.05:
            break

    gyro_y.reset_angle(0)
    gyro_y_offset = gyro_y_sum / GYRO_CALIBRATION_LOOP_COUNT

# Wechselt Zustand und sendet an Server
def switchState_and_send(sensor, new_state):
    global prev_x_state, prev_y_state, prev_button_state
    
    if sensor == "X":
        if new_state != prev_x_state:
            print("Gyro-X: "+str(prev_x_state)+"->"+str(new_state)+" | X:"+str(gyro_x.angle()))
            prev_x_state = new_state
            ev3.screen.clear()
            print("X-"+str(new_state))
            mbox.send("X-"+str(new_state))
            print("Sent X")
            wait(500)


    elif sensor == "Y":
        if new_state != prev_y_state:
            print("Gyro-Y: "+str(prev_y_state)+"->"+str(new_state)+" | Y:"+str(gyro_y.angle()))
            prev_y_state = new_state
            print("Y-"+str(new_state))
            mbox.send("Y-"+str(new_state))
            print("Sent Y")
            wait(500)


    elif sensor == "BUTTON":
        if new_state != prev_button_state:
            print("Button: "+str(prev_button_state)+"->"+str(new_state))
            print("Gyro-X: "+str(gyro_x.angle()) + ", Gyro-Y: "+str(gyro_y.angle()))
            prev_button_state = new_state
            print("BUTTON-"+str(new_state))
            mbox.send("BUTTON-"+str(new_state))
            print("Button")
            wait(500)





# Timer für regelmäßige Neukalibrierung
calibration_timer = StopWatch()
CALIBRATION_INTERVAL = 60000  # 60 Sekunden

# Verbindung zum Server
print('Verbindung wird hergestellt...')
ev3.screen.clear()
ev3.screen.print('\nVerbinde mit \nServer...')
client.connect(SERVER)
print('Verbunden!')
ev3.screen.clear()
ev3.screen.print('\nVerbunden!')

# Anfängliche Kalibrierung der Gyrosensoren
calibrateGyro_X()
calibrateGyro_Y()
ev3.screen.clear()
ev3.screen.print('\nJOYSTICK')

# Hauptschleife
while True:
    # Regelmäßige Neukalibrierung
    if calibration_timer.time() > CALIBRATION_INTERVAL:
        ev3.screen.clear()
        ev3.screen.print('\nRe-Kalibrierung....')
        calibrateGyro_X()
        calibrateGyro_Y()
        calibration_timer.reset()
        ev3.screen.clear()

    # Gyrosensordaten mit Offsetkorrektur und Filterung
    x_raw = gyro_x.angle() - gyro_x_offset
    y_raw = gyro_y.angle() - gyro_y_offset

    # Exponentielle Glättung anwenden
    x_filtered = SMOOTHING_FACTOR * x_raw + (1 - SMOOTHING_FACTOR) * x_filtered
    y_filtered = SMOOTHING_FACTOR * y_raw + (1 - SMOOTHING_FACTOR) * y_filtered

    # Re-Calibrate
    if x_filtered <= -11:
        gyro_y.reset_angle(-11)
    if x_filtered >= 10:
        gyro_y.reset_angle(10)
    if y_filtered <= -9:
        gyro_y.reset_angle(-9)
    if y_filtered >= 10:
        gyro_y.reset_angle(10) 

    # Gyrosensorstatus überprüfen und entsprechende Aktionen ausführen
    if x_filtered <= -8 and prev_x_state != NEGATIVE:
        switchState_and_send("X", "NEGATIVE")
    elif x_filtered >= 7 and prev_x_state != POSITIVE:
        switchState_and_send("X", "POSITIVE")
    elif (x_filtered < 7 and x_filtered > -8) and prev_x_state != NEUTRAL:
        switchState_and_send("X", "NEUTRAL")

    if y_filtered <= -6 and prev_y_state != NEGATIVE:
        switchState_and_send("Y", "NEGATIVE")
    elif y_filtered >= 7 and prev_y_state != POSITIVE:
        switchState_and_send("Y", "POSITIVE")
    elif (y_filtered < 7 and y_filtered > -6) and  prev_y_state != NEUTRAL:
        switchState_and_send("Y", "NEUTRAL")

    if button.pressed() and prev_button_state != "PRESSED":
        switchState_and_send("BUTTON", "PRESSED")
    elif not button.pressed() and prev_button_state != "RELEASED":
        switchState_and_send("BUTTON", "RELEASED")


    # Manuelle Re-Kalibrierung
    if Button.LEFT in ev3.buttons.pressed():
        ev3.screen.clear()
        ev3.screen.print('\nRe-Kalibrierung....')
        calibrateGyro_X()
        calibrateGyro_Y()
        ev3.screen.clear()
