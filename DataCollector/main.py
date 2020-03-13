import argparse
#from networkCommunication import network
#from serialCommunication import serial

# Constant variables
CFGFILE: str = "config.cfg"
AVAILABLEMODES: list = ["network", "serial"]
#AVAILABLEFUNCTIONS: list = [network, serial]

# Data storage
data: dict = {}

# Checks if the given configuration file defines the given element
def cfgDefines(cfg: str, element: str, choices: list = []):
    try:
        with open(cfg, "r") as f:
            for line in f.readlines():
                content = line.split("=")
                if len(choices) != 0:
                    if content[0] == element and content[1].strip() in choices:
                        break
                else:
                    if content[0] == element and content[1].strip() != "":
                        break
            else: 
                return False
            return True
    except:
        return False

def main():
    #########################################################################
    #   CREATES THE CONFIG FILE AND PUTS THE DATA FROM THE CONSOLE INTO IT  #
    #########################################################################

    # Create parser with arguments
    parser = argparse.ArgumentParser(description="Puts data from production line to a file")
    parser.add_argument(
        "-f", "--filename", 
        required=not cfgDefines(CFGFILE, "filename")
    )
    parser.add_argument(
        "-m", "--mode", 
        choices=AVAILABLEMODES, 
        required=not cfgDefines(CFGFILE, "mode", AVAILABLEMODES)
    )
    parser.add_argument(
        "-k", "--apikey",
        required=not cfgDefines(CFGFILE, "apikey")
    )

    try:
        # Reads the data from the config file to the data dictionary
        with open(CFGFILE, "r") as f:
            fileContent = f.readlines()
            for row in fileContent:
                currentElement = row.split("=")
                if (len(currentElement) == 2):
                    data[currentElement[0]] = currentElement[1].strip() # .strip() -> clears leading and trailing whitespaces

        # If there were any changes made to the arguments then update the dictionary
        args = parser.parse_args()
        argsDict = vars(args)

        # Update the data dictionary
        for k, v in argsDict.items():
            if v != None:
                data[k] = v

        # Also update the file
        with open(CFGFILE, "w") as f:
            for k, v in data.items():
                f.write(f"{k}={v}\n")
    except:
        # If the config file does not exist then add it to the data
        args = parser.parse_args()
        data["filename"] = args.filename
        data["mode"] = args.mode
        data["apikey"] = args.apikey

        # Also create the config file
        with open(CFGFILE, "x") as f:
            for k, v in data.items():
                f.write(f"{k}={v}\n")
    
    #####################################################################
    #   GETS THE DATA FROM THE WORKSTATION ACCORDING TO THE GIVEN MODE  #
    #####################################################################


if __name__ == "__main__":
    main()