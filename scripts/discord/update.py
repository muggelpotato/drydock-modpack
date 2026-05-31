import os
import sys
import json
import urllib.request
import urllib.error

def load_env():
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'").strip('"')

def save_msg_id(msg_id):
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    lines = []
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            lines = [l for l in f if not l.startswith("DISCORD_MESSAGE_ID=")]
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    lines.append(f"DISCORD_MESSAGE_ID={msg_id}\n")
    with open(env_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

def main():
    load_env()
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    message_id = os.environ.get("DISCORD_MESSAGE_ID")
    
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL is missing in .env", file=sys.stderr)
        sys.exit(1)

    config_path = os.path.join(os.path.dirname(__file__), "message.json")
    with open(config_path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    url = f"{webhook_url.rstrip('/')}/messages/{message_id}?wait=true" if message_id else f"{webhook_url}?wait=true"
    if "?with_components=true" not in url and "&with_components=true" not in url:
        url += ("&" if "?" in url else "?") + "with_components=true"
        
    method = "PATCH" if message_id else "POST"
    
    print("Updating Discord announcement...")
    req = urllib.request.Request(
        url,
        headers={"Content-Type": "application/json", "User-Agent": "DrydockDiscordUpdater/1.0"},
        method=method,
        data=json.dumps(payload).encode("utf-8")
    )
    
    try:
        with urllib.request.urlopen(req) as r:
            res = json.loads(r.read().decode("utf-8"))
            new_id = res.get("id")
            print(f"SUCCESS: Announcement updated! Message ID: {new_id}")
            if new_id and new_id != message_id:
                save_msg_id(new_id)
                print("Saved new Message ID to .env file.")
    except Exception as e:
        print(f"ERROR: Webhook execution failed: {e}", file=sys.stderr)
        if isinstance(e, urllib.error.HTTPError):
            print(f"Response: {e.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
