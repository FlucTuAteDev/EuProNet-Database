from flask import Flask, request
from datetime import datetime
import argparse

# Constant variables
CFGFILE: str = "config.cfg"
AVAILABLECOUNTRYCODES: list = ["HU", "DE", "NO", "IS", "CZ", "BE"]
AVAILABLEMODES: list = ["network", "serial"]

# Data storage
data: dict = {}

# Checks if a file exists
def fileExists(file: str):
    try:
        with open(file, "r"):
            return True
    except:
        return False

def main():
    #########################################################################
    #   CREATES THE CONFIG FILE AND PUTS THE DATA FROM THE CONSOLE INTO IT  #
    #########################################################################

    existsCfg = fileExists(CFGFILE) # Checks if the configuration file exists

    # Create parser with arguments
    parser = argparse.ArgumentParser(description="Puts data from production line to a file") 
    parser.add_argument(
        "-c", "--country", 
        choices=AVAILABLECOUNTRYCODES, 
        required=not existsCfg
    )
    parser.add_argument(
        "-f", "--filename", 
        required=not existsCfg
    )
    parser.add_argument(
        "-m", "--mode", 
        choices=AVAILABLEMODES, 
        required=not existsCfg
    )

    if existsCfg:
        # Reads the data from the config file to the data dictionary
        with open(CFGFILE, "r") as f:
            fileContent = f.readlines()
            for row in fileContent:
                currentElement = row.split("=")
                data[currentElement[0]] = currentElement[1].strip()

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
    else:
        # If the config file does not exist then add it to the data
        args = parser.parse_args()
        data["country"] = args.country
        data["filename"] = args.filename
        data["mode"] = args.mode

        # Also create the config file
        with open(CFGFILE, "x") as f:
            for k, v in data.items():
                f.write(f"{k}={v}\n")
    
    #####################################################################
    #   GETS THE DATA FROM THE WORKSTATION ACCORDING TO THE GIVEN MODE  #
    #####################################################################



# def network():
#     # Instantiates a new flask application
#     app = Flask(__name__)
#     # On the root path the result() method runs
#     @app.route('/', methods=['POST'])
#     def result():
#         # Initialize posted data
#         apiKey = request.form['apiKey']
#         time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
#         buttons = request.form['buttons']
#         discarded = request.form['discarded']
#         finished = request.form['finished']

#         # If the APIs match
#         if apiKey == APIKEYVALUE:
#             # Write data to the output file
#             with open(FILENAME, "a") as f:
#                 f.write(f"{time};{buttons};{discarded};{finished}\n")
#         else:
#             return "APIs don't match!"
        
#         return "Written successfully!"

#     # If this python script is the main script running than start the instantiated application
#     # on host 0.0.0.0, because that way it can be accessed from home network
#     if __name__ == "__main__":
#         app.run(host="0.0.0.0")

if __name__ == "__main__":
    main()