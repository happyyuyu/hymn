''' This file serves as a mini-server that handles URL requests from electron'''

import time
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/test")
def hello():
    return "Hello! Produced by Python."
    # return render_template("name.html", name="Hazhou")

if __name__ == "__main__":
    #time.sleep(5)
    app.run(host='127.0.0.1', port=5000)