import serial

APIKEYVALUE = "wV9ysymCPn9yTYcilpIT"
serialCommunicationPort = 'COM8'
baudrate = 115200
isApiKey = False

ser = serial.Serial(serialCommunicationPort, baudrate, timeout=1) # Starts the serial communication with the given parameters
file = open("buttonPresses.csv", "a")
while 1:
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        rawInputData = str(ser.readline()).replace("\r\n", "")
        print(rawInputData)
        dataUnits = rawInputData.split("&")
        for i in range(len(dataUnits)):
            if i == 0:
                isApiKey = dataUnits[i][1] == APIKEYVALUE
                continue
            if isApiKey:
                file.write(dataUnits[i][1] + ";")