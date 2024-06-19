import serial
import time

# Configure the serial connection (the port may vary depending on your system)
ser = serial.Serial('COM3', 115200, timeout=1)  # Replace 'COM3' with your port

def send_command(command):
    ser.write(command.encode())
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    return response

def main():
    # Example command to send
    command = "MOVE_TO_POSITION 1"
    response = send_command(command)
    print("EV3 Response:" ,{response})

if __name__ == "__main__":
    main()