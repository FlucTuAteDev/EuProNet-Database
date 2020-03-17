import argparse
import re
from pathlib import Path

CFGFILE: str = Path(rf"{__file__}\..").absolute()/'config.cfg' #  Configuration file path
AVAILABLE_MODES: list = ["network", "serial"]
# Required configurations (name -> value regex)
CONFIG_REQUIREMENTS = {
    "filename": ".+",
    "mode": '|'.join(["^{}$".format(x) for x in AVAILABLE_MODES]), #  Pattern: ^a$|^b$|^c$...
    "apikey": ".+",
    "networkPort": "[0-9]{1,5}",
    "serialPort": ".+"
}

def main():
    # Configuration storage
    cfg: dict = {}
    # Set all the config values to None
    # If cfg[key] remains None the parser knows to require that key
    for key in CONFIG_REQUIREMENTS.keys():
        cfg[key] = None
        
    # Read correct data into the cfg storage
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
    args = vars(parser.parse_args())

    # Update the cfg dictionary with the given arguments
    for key, value in args.items():
        if value is not None and re.match(CONFIG_REQUIREMENTS[key], value):
            cfg[key] = value

    # Also update the file with the given arguments
    with open(CFGFILE, "w") as f:
        for k, v in cfg.items():
            f.write(f"{k}={v}\n")

##if __name__ == "__main__":
main()
