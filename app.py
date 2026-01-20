from flask import Flask, request
import requests
import os

# आपका डेटा
API_TOKEN = '8474505122:AAF46ORltV2Z8XypWDRh8K8IjhKLVMPRPyA'
REFERRAL_LINK = "https://1wkaws.com/?p=3l7z"
PROMO_CODE = "UXQ1WIN"

app = Flask(__name__)

def send_message(chat_id, text):
    # यह फंक्शन सीधा Telegram API को मैसेज भेजता है
    url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    # मैसेज भेजें
    r = requests.post(url, json=payload)
    print(f"📤 Sent Reply: {r.status_code} - {r.text}", flush=True)

@app.route('/' + API_TOKEN, methods=['POST'])
def webhook():
    # 1. डेटा रिसीव करें
    data = request.json
    print(f"📩 NEW DATA: {data}", flush=True)  # यह Log में पक्का दिखेगा

    # 2. चेक करें कि क्या यह मैसेज है?
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        
        # अगर टेक्स्ट है, तो उसे पढ़ें
        if "text" in data["message"]:
            incoming_text = data["message"]["text"].lower()
            
            # 3. अगर Start या Hy लिखा है, तो जवाब भेजें
            if incoming_text in ['/start', 'hy', 'hi', 'hello']:
                msg = (
                    f"🚀 **Welcome to 1win!** 🚀\n\n"
                    f"💰 **Register Now:**\n👉 {REFERRAL_LINK}\n\n"
                    f"🔥 **Code:** `{PROMO_CODE}`"
                )
                send_message(chat_id, msg)
            else:
                # अगर कुछ और लिखा है तो भी टेस्ट के लिए जवाब दें
                send_message(chat_id, "Type 'hy' or '/start' to get the link.")

    return "OK", 200

@app.route("/")
def index():
    return "<h1>Bot is Running in Direct Mode!</h1>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
