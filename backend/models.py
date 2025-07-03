import uuid
from datetime import datetime, timezone

def format_event(event_type, payload):
    author = payload["sender"]["login"]

    # Default timestamp: now in ISO with UTC 'Z'
    timestamp = datetime.now(timezone.utc).isoformat()

    # For push: convert GitHub UNIX pushed_at to ISO 8601
    if event_type == "push":
        pushed_at_unix = payload.get("repository", {}).get("pushed_at")
        if pushed_at_unix:
            timestamp = datetime.fromtimestamp(pushed_at_unix, tz=timezone.utc).isoformat()
        return {
            "type": "push",
            "author": author,
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": timestamp,
            "request_id": str(uuid.uuid4())
        }

    elif event_type == "pull_request":
        pr = payload["pull_request"]
        action = payload.get("action")
        is_merged = pr.get("merged", False)

        timestamp = pr.get("created_at", timestamp)

        event = {
            "type": "pull_request",
            "author": pr["user"]["login"],
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": timestamp,
            "request_id": str(pr["id"])
        }

        if action == "closed" and is_merged:
            event["type"] = "merge"
            event["timestamp"] = pr["merged_at"]

        return event

    return None
