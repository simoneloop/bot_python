import telebot
import cv2
import shutil
import os
from .Real import inference_realesrgan

# from .ReaReal-ESRGAN import inference_realesrgan
API_TOKEN = '5541852432:AAFPebccjkqifFbHzjTL2ZrqGntWNZ77AQw'
bot = telebot.TeleBot(API_TOKEN)
@bot.message_handler(commands=['help', 'start'])
def send_welcome(msg):
    bot.send_message(msg.chat.id, """\
            Hi there, I am UPI. I am ready to UPSCALE your IMAGE
            \
            """)


@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'voice']) # list relevant content types
def addfile(message):
    from io import BytesIO
    import numpy as np
    print(message.photo[-1])
    photo = message.photo[-1]
    id=photo.file_id
    # img = cv2.imdecode(np.fromstring(BytesIO(photo.download_as_bytearray()).getvalue(), np.uint8), 1)

    print(id)

    bot.send_message(message.chat.id,"ricevuto file")
    file_info = bot.get_file(id)
    downloaded_file = bot.download_file(file_info.file_path)
    # cv2.imwrite("prova.jpg", img)
    with open("prova.png", 'wb') as new_file:
        new_file.write(downloaded_file)


upload_folder = 'upload'
result_folder = 'results'


if os.path.isdir(upload_folder):
    shutil.rmtree(upload_folder)
if os.path.isdir(result_folder):
    shutil.rmtree(result_folder)
os.mkdir(upload_folder)
os.mkdir(result_folder)

main( "-n RealESRGAN_x4plus", "-i upload", "--outscale 4", "--face_enhance")

bot.polling()