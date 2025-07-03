from flask import Flask, request, jsonify
from flask_cors import CORS
from db import events_collection
from models import format_event
import os
app=Flask(__name__)
CORS(app)
port=os.getenv("PORT",5000)

@app.route("/webhook", methods=["POST"])
def github_webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json
    event = format_event(event_type, payload)

    if event:
        result = events_collection.insert_one(event)
        print("🟢 Inserted into MongoDB with ID:", result.inserted_id)
    else:
        print("⚠️ No event inserted (invalid or unhandled event type)")

    return jsonify({"status": "received"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    events = list(events_collection.find({}, {"_id": 0}))
    return jsonify(events)

if __name__ == "__main__":
    app.run(port=port)