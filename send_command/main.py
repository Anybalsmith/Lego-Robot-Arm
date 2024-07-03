#!/usr/bin/env python3

from pybricks.messaging import BluetoothMailboxClient, TextMailbox

# This demo makes your PC talk to an EV3 over Bluetooth.
#
# This is identical to the EV3 client example in ../bluetooth_client
#
# The only difference is that it runs in Python3 on your computer, thanks to
# the Python3 implementation of the messaging module that is included here.
# As far as the EV3 is concerned, it thinks it just talks to an EV3 client.
#
# So, the EV3 server example needs no further modifications. The connection
# procedure is also the same as documented in the messaging module docs:
# https://docs.pybricks.com/en/latest/messaging.html
#
# So, turn Bluetooth on on your PC and the EV3. You may need to make Bluetooth
# visible on the EV3. You can skip pairing if you already know the EV3 address.

# Replace with your EV3 Bluetooth address
SERVER = 'CC:78:AB:DC:A8:47'

client = BluetoothMailboxClient()
mbox = TextMailbox("greeting", client)

print("establishing connection...")
client.connect(SERVER)
print("connected!")

# Envoyez la commande "pick 2 place 4"
command = "pick 2 place 4"
mbox.send(command)
print(f"Command '{command}' sent!")

# Attendez et lisez la réponse du serveur (EV3)
mbox.wait()
response = mbox.read()
print("EV3 Response:", response)