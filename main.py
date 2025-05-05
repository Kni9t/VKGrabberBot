import telebot
import json
from telebot import types

from VKGrabber import VKGrabber

VKCollector = VKGrabber("token")

bot = telebot.TeleBot(open('botKey').read())