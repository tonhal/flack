import os

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = []
messages = []

@app.route("/")
def index():
    return render_template("base.html", channels=channels)

@app.route("/messages", methods=["POST"])
def get_messages():
    channel = request.form.get("channel")
    return jsonify({"success": True, "messages": messages})

@socketio.on("add new channel")
def new_channel(data):
    channel_name = data["channel"]
    if not channel_name in channels:
        channels.append(channel_name)
        emit("add channel", {"channel": channel_name}, broadcast=True)
    else:
        emit("exception", {"error_message": "There is already a channel with this name. Choose a different name."})

@socketio.on("add new message")
def new_message(data):
    new_message = {
        "channel": data["channel"],
        "message_content": data["message_content"],
        "message_sender": data["sender"]
    }
    messages.append(new_message)
    emit("add message", {"message": new_message}, broadcast=True)