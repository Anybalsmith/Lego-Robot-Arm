# Projet : Robot arm pick and place

**IT Project Management Project**

The aim of the project is to carry out "pick and place" using a Lego robotic arm fitted with a gripper. This project consists in two parts:

- the vision part, where a Python program located on the computer detects using a webcam which cubes should be picked by the robot arm, their position and their color.
- the control part, where a Python program located on the EV3 brick picks the cubes from their current position and places them in a container based on their color.

As the two parts run on different devices, the computer has to send the instructions (`pickandplace(start_position, end_position)`) to the EV3 brick. Sadly, we encountered technical issues with the Bluetooth communication between the computer and the EV3 brick, so there is currently no communication between the two parts.

## Prerequisites

On the PC:

- Assuming you use VS Code, install the [LEGO® MINDSTORMS® EV3 MicroPython
  ](https://marketplace.visualstudio.com/items?itemName=lego-education.ev3-micropython) VS Code extension

## The vision part

See `vision/main.py`.

It works by looking at circles around so-called `predefined_positions`, and checking the percentage of pixels that are of each cube's color (it works for the 3 cubes: blue, green and red). If this percentage is above 5%, it means that the cube is present at this position. The green cubes go in the container at position 1, the green cubes at position 4, and there's no 3rd container for the red cubes (though it's easy to change that) as we use 2 of the 4 available positions to place cubes and the 2 others for 2 containers.

From there, if for example we detect a green cube at position 3, we print `pick 3 place 1` to the console, which is enough information for the control part to take over.

To run this part, just run the `vision/main.py` file on the computer after having connected the webcam.

## The control part

See `go_to_position/main.py`.

This program allows the robot arm to pick a cube at a predefined position (between 1 and 4) and place it at another predefined position (between 1 and 4).

In our setup, we placed our green container at position 1 and our blue container at position 4, so we pick cubes in positions 2 and/or 3 and place them in positions 1 and/or 4.

To run this part, connect the EV3 brick to the computer and run the `go_to_position/main.py` file on it. If you're using VS Code, the `LEGO® MINDSTORMS® EV3 MicroPython` extension should have installed `ev3dev` as a debugger, so you can just press F5 to run the program on the EV3 brick.

Currently, there is no communication between the vision part and the control part, so you have to type the commands outputted by the vision part in your terminal to move the arm, such as `pick 3 place 1` to move the cube at position 3 to the container at position 1.

## Other files

- `robotarm_motor` folder: Allows you to control manually each robot motor
- `useful code` folder : Not all the code within it works, but it might help someone continuing the project.
- `useful code/send_command` and `useful code/pick_and_place_bluetooth` folders: code intended to send the "pick and place" to the robot via bluetooth, but the bluetooth communication between the computer and the brick is not working
- `useful code/control_part` folder: contains an implementation of inverse kinematic model of the robot (Denavit-Hartenberg convention) https://drive.google.com/drive/folders/0ByaIRKZHDhW-a0dQTS00cVF0WTg?resourcekey=0-q5wPMnFpUDWotvQ-APGziQ some slides may be useful for the modelisation in chapter 2 (it's in french sorry)
