import telebot
import json
from telebot import types

from VKGrabber import VKGrabber

VKCollector = VKGrabber("Parameters/token")
bot = telebot.TeleBot(open('Parameters/botKey').read())
channelParams = json.load('channel_parameters.json')

bot.send_message(chat_id = channelParams['channel_username'], text = 'Hello world!')