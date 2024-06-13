#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A
from ev3dev2.motor import SpeedPercent
from time import sleep

# Init Motor
motor = LargeMotor(OUTPUT_A)
print("start", motor.position)
sleep(2)
# Set the position of the motor to zero
motor.position = 0
print("init",motor.position)
sleep(2)
# move the motor (e.g. 50% power for 2 seconds)
motor.on(SpeedPercent(50))
sleep(2)
motor.off()
print("end",motor.position)
# Determine the current position of the motor
position = motor.position
