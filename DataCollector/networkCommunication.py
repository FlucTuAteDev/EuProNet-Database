from flask import Flask, request
from datetime import datetime

def network(filename: str, apiKey: str):
    # Instantiates a new flask application
    app = Flask(__name__)
    # On the root path the result() method runs
    @app.route('/', methods=['POST'])
    def result():
        # Initialize posted data
        requestApiKey = request.form['apiKey']
        time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        state = request.form['state']

        # If the APIs match
        if apiKey == requestApiKey:
            # Write data to the output file
            with open(filename, "a") as f:
                f.write(f"date:{time};state:{state}\n")
        else:
            return "APIs don't match!"
        
        return "Written successfully!"
        
    app.run(host="0.0.0.0")