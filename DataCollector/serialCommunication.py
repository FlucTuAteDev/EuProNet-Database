import serial
import time
# filename: str = "", apikey: str = "", port: str = "", baudrate: int = 9600
def serialComm(**kwargs):
    with serial.Serial(kwargs) as ser:
        while 1:
            # If there is incoming connection
            if ser.inWaiting() > 0:
                # Write the recieved data to the given file
                with open(kwargs["filename"], "a") as f:
                    for data in ser.readline().split("&"):
                        (key, value) = data.split("=")
