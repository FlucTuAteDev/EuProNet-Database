from serial import serialwin32 as serial
import time
from datetime import datetime
# filepath: str = "", apikey: str = "", port: str = "", baudrate: int = 9600
def serialComm(filepath: str = "", apikey: str = "", port: str = "COM7", baudrate: int = 115200):
    with serial.Serial(port=port, baudrate=baudrate) as ser:
        while 1:
            # If there is incoming connection
            if ser.inWaiting() > 0:
                date = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
                # Write the recieved data to the given file
                with open(filepath, "a") as f:
                    f.write(f"date:{date};{ser.readline()}")
