import telebot
import json
from telebot import types

from VKGrabber import VKGrabber

VKCollector = VKGrabber("Parameters/token")
bot = telebot.TeleBot(open('Parameters/botKey').read())
