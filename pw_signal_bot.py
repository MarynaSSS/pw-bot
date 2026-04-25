import os
from flask import Flask, request, jsonify
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")
WEBHOOK_KEY = os.environ.get("WEBHOOK_KEY", "pw_secret_2024")
PORT = int(os.environ.get("PORT", 5000))

app = Flask(__name__)

def send_telegram(text):
requests.post(
f"https://api.telegram.org/bot8103609497:AAGLkpf1EGjtD7OU_G-UIbHlizmhMDXim8U/sendMessage",
json={"chat_id": CHAT_ID, "text": text},
timeout=8
)

@app.route("/webhook", methods=["POST"])
def webhook():
key = request.args.get("key", "")
if key != WEBHOOK_KEY:
return jsonify({"error": "unauthorized"}), 401
raw = request.data.decode("utf-8").strip()
send_telegram(f"PW SIGNAL\n{raw}")
return jsonify({"ok": True})

@app.route("/ping")
def ping():
return jsonify({"status": "alive"})

@app.route("/")
def index():
return "PW Bot running", 200

if __name__ == "__main__":
send_telegram("PW Signal Bot started!")
app.run(host="0.0.0.0", port=PORT)


