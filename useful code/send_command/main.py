#!/usr/bin/env python3
import time
from pybricks.messaging import BluetoothMailboxServer, TextMailbox


# SERVER = 'CC:78:AB:DC:A8:47'


server = BluetoothMailboxServer()
mbox = TextMailbox("command", server)

print("Waiting for connection...")
server.wait_for_connection()
print("Connected!")

# In this program, the server waits for the client to send the first message
# and then sends a reply.
print('wait')
mbox.wait()
print(mbox.read())
mbox.send("hello to you!")


# Send command "pick 2 place 4"
command = "pick 2 place 4"
mbox.send(command)
print(f"Command '{command}' sent!")


response = mbox.read()
print("EV3 Response:", response)