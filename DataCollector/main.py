import argparse
import re
import networkCommunication
import serialCommunication

# Constant variables
CFGFILE: str = "config.cfg"
AVAILABLEMODES: list = ["network", "serial"]

# Data storage
data: dict = {}


def listToRg(l: list):
    result: list = []
    for element in l:
        result.append(f"^{element}$")
    return '|'.join(result)


# Checks if the configuration file defines the given element
# with the either given or not given choices
def cfgDefines(element: str, cfg: str = CFGFILE, regex: str = ".*"):
    try:
        with open(cfg, "r") as f:
            for line in f.readlines():
                (key, value) = line.split("=", 1)
                if key == element and re.match(regex, value):
                    break
            else:
                return False
            return True
    except:
        return False


def main():
    # PUT DATA INTO CONFIG FILE #

    # Create parser with arguments
    parser = argparse.ArgumentParser(
        description="Puts data from production line to a file"
    )
    parser.add_argument(
        "-f", "--filename",
        required=not cfgDefines("filename")
    )
    parser.add_argument(
        "-m", "--mode",
        choices=AVAILABLEMODES,
        required=not cfgDefines("mode", regex=listToRg(AVAILABLEMODES))
    )
    parser.add_argument(
        "-k", "--apikey",
        required=not cfgDefines("apikey")
    )
    parser.add_argument(
        "-n", "--networkPort",
        type=int
    )
    parser.add_argument(
        "-s", "--serialPort"
    )
    

    # If the config file exists then read its data to the data dictionary
    try:
        with open(CFGFILE, "r") as f:
            fileContent = f.readlines()
            for row in fileContent:
                currentElement = row.split("=")
                if (len(currentElement) == 2):
                    data[currentElement[0]] = currentElement[1].strip()
    # If it doesn't exist then create the file
    except:
        with open(CFGFILE, "x"):
            pass

    # Parse the arguments to a dictionary
    args = parser.parse_args()
    argsDict = vars(args)

    # Update the data dictionary with the given arguments
    for k, v in argsDict.items():
        if v is not None:
            data[k] = v

    # Also update the file with the given arguments
    with open(CFGFILE, "w") as f:
        for k, v in data.items():
            f.write(f"{k}={v}\n")

##if __name__ == "__main__":
main()
