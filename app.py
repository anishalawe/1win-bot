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

# DEBUG: यह हर तरह के मैसेज का रिप्लाई करेगा
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(f"DEBUG: Message received from {message.from_user.first_name}: {message.text}")
    try:
        # हम जानबूझकर बिना डिज़ाइन के मैसेज भेज रहे हैं ताकि कोई एरर न आए
        bot.reply_to(message, f"Test Successful!\nLink: {REFERRAL_LINK}\nCode: {PROMO_CODE}")
        print("DEBUG: Reply sent successfully!")
    except Exception as e:
        print(f"DEBUG: Error sending message: {e}")

@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    current_url = request.host_url.replace('http://', 'https://')
    bot.set_webhook(url=current_url + API_TOKEN)
    return f"<h1>Bot Updated. Webhook set to: {current_url + API_TOKEN}</h1>", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
