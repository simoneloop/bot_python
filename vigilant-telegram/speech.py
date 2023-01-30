import speech_recognition as sr
import openai
import telebot
from telebot import types
from pydub import AudioSegment
from gtts import gTTS
from io import BytesIO


import os
api_key = os.environ.get("OPENAI_KEY")

openai.api_key=api_key
API_TOKEN ='5854352780:AAHtJ7YGBHSASJ7OmyIfJKa4FWbv00qsJPM'


bot = telebot.TeleBot(API_TOKEN)
@bot.message_handler(commands=['help', 'start'])
def send_welcome(msg):
    
    bot.send_message(msg.chat.id, """\
            Hello Master, let me translate your phrases
            \
            """)

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    
    try:
            r = sr.Recognizer()
            with open('./new_file.ogg', 'wb') as new_file:
                new_file.write(downloaded_file)
            sound = AudioSegment.from_ogg("./new_file.ogg")
            name_from_user="./output-"+message.chat.username+".wav"
            sound.export(name_from_user, format="wav")

            with sr.AudioFile(name_from_user) as source:
                audio_data = r.record(source)
                
            print("Recognizing Now .... ")
            promptt=r.recognize_google(audio_data,language="it-IT")
            print("You have said \n" + promptt)
            prompts="devi solo tradurre in inglese: "+promptt
            completion=openai.Completion.create(engine="text-davinci-003",prompt=prompts,max_tokens=1000)
            phrase=completion.choices[0]['text']
            tts=gTTS(text=phrase, lang="en")
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            
            bot.send_audio(chat_id=message.chat.id, audio=fp)
            print(phrase)


    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "stiamo ricevendo troppe richieste, risponderemo a breve, in caso contrario prova a reinviare il messaggio")

bot.polling()
