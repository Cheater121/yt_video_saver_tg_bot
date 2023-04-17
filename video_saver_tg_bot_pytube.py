import telebot
import os
from pytube import YouTube

bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Hello! Please send me a YouTube video link to download.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
        if not message.text.startswith("http"):
        	bot.send_message(message.chat.id, "Please send a valid link.")
        	return
        try:
        	yt = YouTube(message.text)
        	stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        	bot.send_message(message.chat.id, "Starting download video.")
        	stream.download(filename='video.mp4')
        except TypeError: #need to find all exeptions
        	bot.send_message(message.chat.id, "Could not download the video. Please try again with a different link.")
        	return
        try:
        	with open("video.mp4", "rb") as f:
        		bot.send_video(message.chat.id, f)
        except FileNotFoundError:
        	bot.send_message(message.chat.id, "Could not find the downloaded video.")
        finally:
        	os.remove("video.mp4")

bot.polling()
