import re
from pathlib import Path
import configHandler
from networkCommunication import networkComm
# TODO: SERIAL COMMUNICATION
# from serialCommunication import serialComm

CFGFILE: str = Path(rf"{__file__}\..").absolute()/'config.cfg' #  Configuration file path
AVAILABLE_MODES: dict = {
    "network": networkComm
    # "serial": serialComm
}
# Required configurations (name -> value regex)
CONFIG_REQUIREMENTS = {
    "filepath": (".+", "Please enter the buffer file's path: "),
    "mode": ('|'.join([f"^{x}$" for x in AVAILABLE_MODES.keys()]), "Please enter the communication mode (network | serial): "),
    "apikey": (".+", "Please enter the api key: "),
    "networkPort": ("[0-9]{1,5}", "Please enter the port you want to run the server on: "),
    "serialPort": (".+", "Please enter the serial port of your device: ")
}

def main():
    cfg = configHandler.configHandler(CONFIG_REQUIREMENTS, CFGFILE)
    cfg.setUserConfigs()
    
    # Run the function of the given mode
    AVAILABLE_MODES[cfg.mode](filepath=cfg.filepath, apikey=cfg.apikey)

if __name__ == "__main__":
    main()
