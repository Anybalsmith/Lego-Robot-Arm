# Projet : Robot arm pick and place

**IT Project Management Project**

The aim of the project is to carry out "pick and place" using a Lego robotic arm fitted with a gripper. This project includes a vision part which consists of detecting the objects to be moved by the camera and their coordinates. Once this has been done, the end effector of our robotic arm will have to move to the coordinates of the box, pick it up (_pick_), then move it to a given position (_place_).

## Prerequisites

On the PC:

- Install the [LEGO® MINDSTORMS® EV3 MicroPython
  ](https://marketplace.visualstudio.com/items?itemName=lego-education.ev3-micropython) VS Code extension

## The vision part

The camera is positioned above the stage at a fixed distance and detects the coordinates of the centre of gravity of each part. It then returns these coordinates to the base reference frame linked to the robot's platform.

## The control part

Control part is located in go_to_position -> main.py 
This program allow robot arm to pick a cube at a prerecorded position (between 1 and 5) and place it at a prerecorded position (between 1 and 5)

robotarm_motor allow you to control manually each robot motor


## Other files


useful code file : This file contain working or not code
    send_command and pick_and_place_bluetooth are code to send pick and place to the robot via bluetooth, the bluetooth communication between computer and brick is not working
    control_part contain an implementation of inverse kinematic model of the robot (Denavit-Hartenberg convention) https://drive.google.com/drive/folders/0ByaIRKZHDhW-a0dQTS00cVF0WTg?resourcekey=0-q5wPMnFpUDWotvQ-APGziQ some slides may be useful for the modelisation in chapter 2 (it's in french sorry)
