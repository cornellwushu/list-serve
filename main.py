import os
import json
from dotenv import load_dotenv
from flask import Flask, request
from datetime import datetime
import list_serve

app = Flask(__name__)
load_dotenv("./local.env")


def build_response(data, code=200):
    return json.dumps(data), code


@app.route("/")
def init():
    return json.dumps("Cornell Wushu")


@app.route("/send_email")
def send_email():
    try:
        email = list_serve.WushuEmail(
            os.environ.get("GMAIL_USER"), os.environ.get("GMAIL_PASSWORD"), "weekly"
        )
        email.send_email(["ps2245@cornell.edu"])
    except Exception as e:
        return build_response(e, 400)
    return build_response("success", 200)


if __name__ == "__main__":
    app.run("localhost", 8080, debug=True)
