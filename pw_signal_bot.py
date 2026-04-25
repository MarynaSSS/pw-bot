import os, logging
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask, request, jsonify
import requests as req_lib

BOT_TOKEN = os.environ.get("BOT_TOKEN", "ВСТАВЬ_ТОКЕН")
CHAT_ID = os.environ.get("CHAT_ID", "ВСТАВЬ_CHAT_ID")
WEBHOOK_KEY = os.environ.get("WEBHOOK_KEY", "pw_secret_2024")
PORT = int(os.environ.get("PORT", 5000))
EST = ZoneInfo("America/New_York")

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
signal_log = []

def send_telegram(text):
try:
r = req_lib.post(
f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
json={"chat_id": CHAT_ID, "text": text,
"parse_mode": "HTML"},
timeout=8)
r.raise_for_status()
return True
except Exception as e:
log.error(f"Telegram: {e}")
return False

def auth(req):
key = req.args.get("key") or req.headers.get("X-Webhook-Key","")
return key == WEBHOOK_KEY

@app.route("/webhook", methods=["POST"])
def webhook():
if not auth(request):
return jsonify({"error": "unauthorized"}), 401
raw = request.data.decode("utf-8", errors="replace").strip()
now = datetime.now(EST).strftime("%H:%M EST")
msg = f"📊 <b>PW СИГНАЛ</b>\n{raw}\n🕐 {now}"
send_telegram(msg)
signal_log.append({"time": now, "raw": raw})
return jsonify({"ok": True})

@app.route("/ping", methods=["GET"])
def ping():
now = datetime.now(EST).strftime("%H:%M EST")
return jsonify({"status": "alive", "time": now})

@app.route("/", methods=["GET"])
def index():
return "<h2>PW Signal Bot running!</h2>", 200

if __name__ == "__main__":
log.info("PW Bot starting...")
send_telegram("🤖 <b>PW Signal Bot запущен!</b>\nЖду сигналы от TradingView 📡")
app.run(host="0.0.0.0", port=PORT, debug=False)
