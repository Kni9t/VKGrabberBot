import telebot
import json
from telebot import types
import sys

from VKGrabber import VKGrabber

with open('parameters.json') as file:
    parametersDict = json.load(file)

VKCollector = VKGrabber(parametersDict['VKToken'])
bot = telebot.TeleBot(parametersDict['botKey'])

bot.send_message(chat_id = parametersDict['channelUsername'], text = 'Hello world!')
# bot.send_photo(chat_id=channel_id, photo=photo, caption='Вот фото!')