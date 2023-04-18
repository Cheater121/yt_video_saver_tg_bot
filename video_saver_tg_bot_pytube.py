import telebot
import os
import logging
from pytube import YouTube

bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Hello! Please send me a YouTube video link to download.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
        #adding logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.ERROR)
        handler = logging.FileHandler('error.log')
        handler.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        if not message.text.startswith("http"):
        	bot.send_message(message.chat.id, "Please send a valid link.")
        	return
        
        try:
        	bot.send_message(message.chat.id, "Starting download video.")
        	yt = YouTube(message.text)
        	stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        	stream.download(filename='video.mp4')
        except Exception as e:
        	logger.exception(f"{e}\n")
        	bot.send_message(message.chat.id, "Could not download the video. Please try again with a different link.")
        	return
        
        try:
        	with open("video.mp4", "rb") as f:
        		bot.send_video(message.chat.id, f)
        		bot.send_message(message.chat.id, "You are welcome! You can send me another link any time, i'll wait!")
        except Exception as e: #FileNotFoundError:
        	logger.exception(f"{e}\n")
        	bot.send_message(message.chat.id, "Could not find the downloaded video.")
        finally:
        	os.remove("video.mp4")

bot.polling()
