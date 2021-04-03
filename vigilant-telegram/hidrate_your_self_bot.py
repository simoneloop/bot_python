import telebot
import threading
import time
API_TOKEN = '1595350660:AAGwE3ltwnTqOxRODIPOCycNgRi-S3wR2ZI'
usersList=[]
bot = telebot.TeleBot(API_TOKEN)
dueOre=7200
treOre=10800



def presentation(msg,wait):
    time.sleep(wait)
    bot.send_message(msg.chat.id,
                     'Bene iniziamo la nostra bevuta, per il momento è settato tutto al valore di default quindi ti avviserò esattamente ogni 2 ore.')


@bot.message_handler(commands=['help', 'start'])
def send_welcome(msg):
    global usersList
    if(not(msg.from_user.id in usersList)):
        bot.send_message(msg.chat.id, """\
        Hi there, I am Hiddi.
        I am ready to keep you idratated
        \
        """)
        usersList.append(msg.from_user.id)
        print("un nuovo utente si è connesso:"+msg.from_user.first_name)
        print(usersList)
        threadP=threading.Thread(presentation(msg,2))
        threadP.start()
        #presentation(msg,2)
        thread = threading.Thread(idrate_user(msg.from_user.id))
        thread.start()
    else:
        bot.send_message(msg.chat.id,'tranquillo, sono già attivo')



def idrate_user(chat_id):
    exist=True
    while(exist):
        time.sleep(dueOre)
        try:
            print("idrato:",chat_id)
            bot.send_message(chat_id, 'Idratati!')
        except:
            print("idratazione non riuscita con:",chat_id)
            usersList.remove(chat_id)
            exist=False




# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
        bot.reply_to(message, 'Non sono qui per dialogare, ma per tenerti idratato.')


bot.polling()