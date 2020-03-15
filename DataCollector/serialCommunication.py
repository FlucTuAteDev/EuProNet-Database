import serial
import time
# filename: str = "", apikey: str = "", port: str = "", baudrate: int = 9600
def serialComm(**kwargs):
    with serial.Serial(kwargs) as ser:
        while 1:
            if ser.inWaiting() > 0:
                serialData = ser.readline()
                serialData = serialData.split("&")
                with open(kwargs["filename"], "a") as f:
                    for data in serialData:
                        dataParts = data.split("=")
                        f.write(f"{dataParts[1]}")
            else:
                time.sleep(1)
