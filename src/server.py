from flask import Flask, render_template
import socket

app = Flask(__name__)
PORT = 8000


def getIP():
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    SOCKET.settimeout(0)
    try:
        SOCKET.connect(("10.254.254.254", 1))
        IP = SOCKET.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        SOCKET.close()
    return IP

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    pass

@app.route("/signup")
def signup():
    pass

if __name__ == "__main__":
    app.run(getIP(), PORT)
