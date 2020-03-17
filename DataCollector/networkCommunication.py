from flask import Flask, request
from datetime import datetime
# Handles incoming data from network and puts it into the file
def networkComm(filepath: str, apikey: str, host: str = '0.0.0.0', port: int = 5000):
    # Instantiates a new flask application
    app = Flask(__name__)
    # On the root path the result() method runs
    @app.route('/', methods=['POST'])
    def result():
        # Initialize posted data
        date = datetime.now().strftime("%Y.%m.%d %H:%M:%S")

        # If the APIs match
        if apikey == request.form['apikey']:
            # Write data to the output file
            with open(filepath, "a") as f:
                f.write(f"date:{date};{';'.join([f'{key}:{value}' for key, value in request.form.items() if key != 'apikey'])}\n")
        else:
            return "APIs don't match!"
        
        return "Written successfully!"
        
    app.run(host=host, port=port)