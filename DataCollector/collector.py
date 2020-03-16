import argparse
import re
from pathlib import Path

def choicesToRg(l: list):
    result: list = []
    for element in l:
        result.append(f"^{element}$")
    return '|'.join(result)

# Constant variables
CFGFILE: str = Path(f"{__file__}\..").absolute()/'config.cfg' #  Configuration file path
AVAILABLE_MODES: list = ["network", "serial"]
CONFIG_REQUIREMENTS = {
    "filename": ".+",
    "mode": choicesToRg(AVAILABLE_MODES),
    "apikey": ".+",
    "networkPort": "[0-9]{1,5}",
    "serialPort": ".+"
}

def main():
    #############################################
    #   READ DATA AND PUT DATA INTO CONFIG FILE #
    #############################################

    # Configuration storage
    cfg: dict = {}
    # Set all the config values to None
    for key in CONFIG_REQUIREMENTS.keys():
        cfg[key] = None
    try:
        with open(CFGFILE, "r") as f:
            # Reads file content in dictionary like form: [[a, b], [c, d]]
            fileContent = [x.split("=", 1) for x in f.readlines()]
            
            # Read in the values from the config file if it's in the correct form
            for content in fileContent:
                try:
                    key, value = [x.strip() for x in content]
                    if key in CONFIG_REQUIREMENTS.keys() and value != "" and re.match(CONFIG_REQUIREMENTS[key], value):
                        cfg[key] = value
                except:
                    pass
    except:
        pass

    # Create parser with arguments
    parser = argparse.ArgumentParser(
        description="Puts data from production line to a file"
    )

    for key, value in cfg.items():
        parser.add_argument(
            f"-{key[0]}", f"--{key}",
            required=(value == None)
        )

    # Parse the arguments to a dictionary
    args = parser.parse_args()
    argsDict = vars(args)

    # Update the data dictionary with the given arguments
    for key, value in argsDict.items():
        if value is not None and re.match(CONFIG_REQUIREMENTS[key], value):
            cfg[key] = value
            break

    # Also update the file with the given arguments
    with open(CFGFILE, "w") as f:
        for k, v in cfg.items():
            f.write(f"{k}={v}\n")

##if __name__ == "__main__":
main()
