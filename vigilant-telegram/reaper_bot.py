import telebot
from telebot import types

MASTER_USERNAME="Finntastico"
API_TOKEN = '6083242096:AAGCOQS_OZkZbd5-930wm9UzZUxgjaR27qA'

cont=0
question=None
answer=None

bot = telebot.TeleBot(API_TOKEN)
@bot.message_handler(commands=['help', 'start'])
def send_welcome(msg):
    if(msg.chat.username==MASTER_USERNAME):
    
        bot.send_message(msg.chat.id, """\
                Hello Master, let me reap your phrases
                \
                """)

@bot.message_handler(func=lambda message: True)
def echo_message(msg):
    global question
    global answer
    if(question is None):
        question=msg.text
        bot.reply_to(msg, "domanda: "+question)
    elif(answer is None):
        answer=msg.text
        bot.reply_to(msg, "risposta: "+answer)
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
        item_yes = types.KeyboardButton("Si")
        item_no = types.KeyboardButton("No")
        markup.add(item_yes, item_no)
        bot.reply_to(msg, "sono corrette? \n"+
                        "question: "+question+"\n"+
                        "answer: "+answer, reply_markup=markup)
       
        
    else:
        bot.send_message(msg.chat.id, "yes master")
        question=None
        answer=None

bot.polling()