from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os


app = Flask(__name__)

MONGO_URI ="mongodb+srv://abdul:Ajstyle12345@abdul-cluster.vzvnqrd.mongodb.net/?retryWrites=true&w=majority&appName=abdul-cluster"
client = MongoClient(MONGO_URI)
db = client["webhookDB"]
events = db["events"]

@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    print(f"🔔 Webhook received: {event_type}")
    print(f"📦 Payload: {data}")

    try:
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
            print("⚠️ Unsupported event type")
            return jsonify({"msg": "Unsupported event"}), 400

        print(f"✅ Inserting event: {event}")
        events.insert_one(event)
        return jsonify({"msg": "Event saved"}), 200

    except Exception as e:
        print("❌ Error while processing event:", e)
        return jsonify({"msg": "Failed to process"}), 500
