from flask import Flask, request
APIKEYVALUE = "wV9ysymCPn9yTYcilpIT"
filename = "buttonPresses.csv"

app = Flask(__name__)
@app.route('/', methods=['POST'])
def result():
    apiKey = request.form['apiKey']
    time = request.form['time']
    buttons = request.form['buttons']

    if apiKey == APIKEYVALUE:
        with open(filename, "a") as f:
            f.write(f"{time};{buttons}\n")
    else:
        return "APIs don't match!"
    
    return "Written successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")