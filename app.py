from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os


app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI") or "mongodb+srv://abdul:Ajstyle123@abdul-cluster.vzvnqrd.mongodb.net/?retryWrites=true&w=majority&appName=abdul-cluster"
client = MongoClient(MONGO_URI)
db = client["webhookDB"]
events = db["events"]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/webhook', methods=['POST'])
def webhook():
    event_type = request.headers.get('X-GitHub-Event')
    data = request.json

    if event_type == "push":
        event = {
            "type": "push",
            "author": data["pusher"]["name"],
            "to_branch": data["ref"].split("/")[-1],
            "timestamp": datetime.utcnow()
        }

    elif event_type == "pull_request":
        pr = data["pull_request"]
        if data["action"] == "closed" and pr["merged"]:
            event = {
                "type": "merge",
                "author": pr["user"]["login"],
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": datetime.utcnow()
            }
        else:
            event = {
                "type": "pull_request",
                "author": pr["user"]["login"],
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": datetime.utcnow()
            }
    else:
        return jsonify({"message": "Unsupported event"}), 400

    events.insert_one(event)
    return jsonify({"message": "Event stored"}), 200

@app.route('/events')
def fetch_events():
    latest = list(events.find().sort("timestamp", -1).limit(10))
    for e in latest:
        e["_id"] = str(e["_id"])
        e["timestamp"] = e["timestamp"].strftime("%d %B %Y - %I:%M %p UTC")
    return jsonify(latest)

if __name__ == '__main__':
    app.run(debug=True)
