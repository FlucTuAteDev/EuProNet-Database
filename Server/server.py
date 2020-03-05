from flask import Flask, request
from datetime import datetime
APIKEYVALUE = "wV9ysymCPn9yTYcilpIT"
filename = "buttonPresses.csv" # The name of the output file

# Instantiates a new flask application
app = Flask(__name__)
# On the root path the result() method runs
@app.route('/', methods=['POST'])
def result():
    # Initialize posted data
    apiKey = request.form['apiKey']
    time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    buttons = request.form['buttons']
    discarded = request.form['discarded']
    finished = request.form['finished']

    # If the APIs match
    if apiKey == APIKEYVALUE:
        # Write data to the output file
        with open(filename, "a") as f:
            f.write(f"{time};{buttons};{discarded};{finished}\n")
    else:
        return "APIs don't match!"
    
    return "Written successfully!"

# If this python script is the main script running than start the instantiated application
# on host 0.0.0.0, because that way it can be accessed from home network
if __name__ == "__main__":
    app.run(host="0.0.0.0")