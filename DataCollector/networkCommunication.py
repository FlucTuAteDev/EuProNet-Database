from flask import Flask, request
from datetime import datetime
# # Handles incoming data from network and puts it into the file
# def networkComm(filename: str, apiKey: str, host: str = "0.0.0.0", port: int = 5000):
#     # Instantiates a new flask application
#     app = Flask(__name__)
#     # On the root path the result() method runs
#     @app.route('/', methods=['POST'])
#     def result():
#         # Initialize posted data
#         date = datetime.now().strftime("%Y.%m.%d %H:%M:%S")

#         # If the APIs match
#         if apiKey == request.form['apiKey']:
#             # Write data to the output file
#             with open(filename, "a") as f:
#                 f.write(f'date:{date};' + ';'.join(['{}:{}'.format(key, value) for key, value in request.form.items()]))
#         else:
#             return "APIs don't match!"
        
#         return "Written successfully!"
        
#     app.run(host=host, port=port)