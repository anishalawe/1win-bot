import telebot
from flask import Flask, request
import os

# आपका टोकन
API_TOKEN = '8474505122:AAF46ORltV2Z8XypWDRh8K8IjhKLVMPRPyA'

bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

# आपका 1win डेटा
REFERRAL_LINK = "https://1wkaws.com/?p=3l7z"
PROMO_CODE = "UXQ1WIN"

@bot.message_handler(func=lambda message: message.text.lower() in ['/start', 'hy', 'hi', 'hello'])
def send_welcome(message):
    response_text = (
        f"🚀 **Welcome to 1win!** 🚀\n\n"
        f"💰 **Register Now & Win Big:**\n"
        f"👉 {REFERRAL_LINK}\n\n"
        f"🔥 **Use Promo Code:** `{PROMO_CODE}`\n"
        f"(Click to copy code)"
    )
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn_link = telebot.types.InlineKeyboardButton("🔗 Register Here", url=REFERRAL_LINK)
    markup.add(btn_link)

    bot.reply_to(message, response_text, parse_mode='Markdown', reply_markup=markup)

@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    # FIX: यहाँ हमने 'http' को 'https' में बदल दिया है ताकि Telegram को सही लिंक मिले
    current_url = request.host_url.replace('http://', 'https://')
    bot.set_webhook(url=current_url + API_TOKEN)
    return "<h1>Bot is Active! Webhook Set Successfully (HTTPS).</h1>", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
