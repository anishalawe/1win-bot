import telebot
from flask import Flask, request
import os
import logging

# 1. लॉगिंग सेटअप (ताकि हर छोटी बात रिकॉर्ड हो)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# आपका टोकन
API_TOKEN = '8474505122:AAF46ORltV2Z8XypWDRh8K8IjhKLVMPRPyA'

bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

REFERRAL_LINK = "https://1wkaws.com/?p=3l7z"
PROMO_CODE = "UXQ1WIN"

# 2. यह हर मैसेज का रिप्लाई करेगा
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    logger.info(f"✅ HANDLER TRIGGERED: User {message.from_user.first_name} said: {message.text}")
    try:
        bot.reply_to(message, f"BOT IS WORKING!\nLink: {REFERRAL_LINK}\nCode: {PROMO_CODE}")
        logger.info("✅ SUCCESS: Reply sent to Telegram!")
    except Exception as e:
        logger.error(f"❌ ERROR sending reply: {e}")

@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    # 3. कच्चा डेटा प्रिंट करें (ताकि पता चले मैसेज आ भी रहा है या नहीं)
    json_string = request.get_data().decode('utf-8')
    logger.info(f"📩 RAW DATA RECEIVED: {json_string}") 
    
    if not json_string:
        logger.error("❌ ERROR: Empty data received!")
        return "!", 200

    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    current_url = request.host_url.replace('http://', 'https://')
    bot.set_webhook(url=current_url + API_TOKEN)
    return f"<h1>Bot Active. Webhook: {current_url + API_TOKEN}</h1>", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
