import telebot
from telebot import types
import os


MASTER_ID=165097266


API_TOKEN =os.environ.get("TOKEN_REAPER")

cont=0
question=None
answer=None

bot = telebot.TeleBot(API_TOKEN)
@bot.message_handler(commands=['help', 'start'])
def send_welcome(msg):
    if(msg.chat.id==MASTER_ID):
        bot.send_message(msg.chat.id, """\
                Hello Master, let me reap your phrases.
                \
                """)
    else:
        bot.send_message(msg.chat.id, """\
                Hello, you are not my master, but i will consider your text.\n Let me reap your phrases.
                \
                """)

@bot.message_handler(commands=['count','c'])
def send_count(msg):
    global cont
    bot.send_message(msg.chat.id, """\
            Number of QA saved in my run: 
            
            \
            """+str(cont))

@bot.message_handler(func=lambda message: True)
def echo_message(msg):
    global question
    global answer
    global cont
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
        bot.send_message(msg.chat.id, "sono corrette? \n"+
                        "question: "+question+"\n"+
                        "answer: "+answer, reply_markup=markup)
    else:
        if(msg.text.lower()=="si" and msg.chat.id==MASTER_ID):
            with open("simoneset.txt", "a") as f:
                f.write("1: "+question+"\n")
                f.write("2: "+answer+"\n")
                f.write("---"+"\n")
            cont+=1

        bot.send_message(msg.chat.id, "yes master")
        question=None
        answer=None
        

bot.polling()