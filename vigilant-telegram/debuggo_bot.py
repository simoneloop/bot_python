import telebot
import threading
import time
API_TOKEN = '1530834504:AAFTXU8n8c__aR1YaaGQW3OBRlcKtpzDiRw'
bot = telebot.TeleBot(API_TOKEN)
START='/start'
junkBot='IdrateYourSelf'#'1595350660'

def send_start():
    bot.send_message(junkBot,START)

send_start()
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
        print(message)
