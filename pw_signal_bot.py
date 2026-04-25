import os
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask, request, jsonify
import requests as req_lib

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")
WEBHOOK_KEY = os.environ.get("WEBHOOK_KEY", "pw_secret_2024")
PORT = int(os.environ.get("PORT", 5000))
EST = ZoneInfo("America/New_York")
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def send_telegram(text):
try:
r = req_lib.post(
f"https://api.telegram.org/bot8103609497:AAGLkpf1EGjtD7OU_G-UIbHlizmhMDXim8U/sendMessage",
json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"},
timeout=8)
r.raise_for_status()
return True
except Exception as e:
log.error(f"Telegram: {e}")
return False

def auth(req):
key = req.args.get("key") or req.headers.get("X-Webhook-Key", "")
return key == WEBHOOK_KEY

@app.route("/webhook", methods=["POST"])
def webhook():
if not auth(request):
return jsonify({"error": "unauthorized"}), 401
raw = request.data.decode("utf-8", errors="replace").strip()
now = datetime.now(EST).strftime("%H:%M EST")
send_telegram(f"📊 PW SIGNAL
{raw}
{now}")
return jsonify({"ok": True})

@app.route("/ping", methods=["GET"])
def ping():
return jsonify({"status": "alive"})

@app.route("/", methods=["GET"])
def index():
return "PW Bot running", 200

if __name__ == "__main__":
send_telegram("🤖 PW Signal Bot запущен! 📡")
app.run(host="0.0.0.0", port=PORT, debug=False)
