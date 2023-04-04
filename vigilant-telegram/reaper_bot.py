import telebot
from telebot import types
import os


MASTER_ID=165097266


API_TOKEN =os.environ.get("TOKEN_REAPER")


question=None
answer=None
isListing=False
list=[]

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
    count=0
    with open("simoneset.txt", "r") as f:
        lines=f.readlines()
        for line in lines:
            if(str(line).strip()=="---"):
                count+=1
    bot.send_message(msg.chat.id, """\
            Number of QA saved in total: 
            \
            """+str(count))



@bot.message_handler(commands=['list','l'])
def toList(msg):
    global isListing
    global list
    if(not isListing):
        isListing=True
        bot.send_message(msg.chat.id,"Ready to list")
    else:
        
        bot.send_message(msg.chat.id,'Prepare list')
        for i in range(len(list)):
            if(i%2==0):
                bot.send_message(msg.chat.id,"question: "+ list[i]+"\n")
            else:
                bot.send_message(msg.chat.id,"answer: "+ list[i]+"\n")
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
        item_yes = types.KeyboardButton("/Si")
        item_no = types.KeyboardButton("/No")
        markup.add(item_yes, item_no)
        bot.send_message(msg.chat.id, "sono corrette? \n", reply_markup=markup)

@bot.message_handler(commands=['si','Si'])
def add(msg):
    global isListing
    global list
    global question
    global answer
    if(not isListing):
        if(msg.chat.id==MASTER_ID):
            with open("simoneset.txt", "a") as f:
                f.write("1: "+question+"\n")
                f.write("2: "+answer+"\n")
                f.write("---"+"\n")

        bot.send_message(msg.chat.id, "yes master")
        isListing=False
        list=[]
        answer=None
        question=None
    else:
        if(msg.chat.id==MASTER_ID):
            with open("simoneset.txt", "a") as f:
                for i in range(len(list)):
                    if(i%2==0):
                        f.write("1: "+list[i]+"\n")
                    else:
                        f.write("2: "+list[i]+"\n")
                        f.write("---"+"\n")
        bot.send_message(msg.chat.id, "yes master")
        isListing=False
        list=[]
        answer=None
        question=None


@bot.message_handler(commands=['no','No'])
def add(msg):
    global isListing
    global list
    global answer
    global question
    isListing=False
    list=[]
    answer=None
    question=None

@bot.message_handler(func=lambda message: True)
def echo_message(msg):
    global question
    global answer
    global cont
    global isListing

    if(not isListing):
        if(question is None):
            question=msg.text
            bot.reply_to(msg, "domanda: "+question)
        elif(answer is None):
            answer=msg.text
            bot.reply_to(msg, "risposta: "+answer)
            markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
            item_yes = types.KeyboardButton("/Si")
            item_no = types.KeyboardButton("/No")
            markup.add(item_yes, item_no)
            bot.send_message(msg.chat.id, "sono corrette? \n"+
                            "question: "+question+"\n"+
                            "answer: "+answer, reply_markup=markup)
            
    else:
        list.append(msg.text.lower())
        


bot.infinity_polling(timeout=10, long_polling_timeout = 5)
