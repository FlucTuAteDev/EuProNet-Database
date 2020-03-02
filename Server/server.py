from flask import Flask, request
APIKEYVALUE = "wV9ysymCPn9yTYcilpIT"
filename = "buttonPresses.csv"

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def result():
    if (request.method == 'POST'):
        apiKey = request.form['apiKey']
        time = request.form['time']
        buttons = request.form['buttons']

        if apiKey == APIKEYVALUE:
            with open(filename, "a") as f:
                f.write(f"{time};{buttons}\n")
        
        return "Written successfully!"
    else:
        return "Not acceptable request"

if __name__ == "__main__":
    app.run(host="0.0.0.0")