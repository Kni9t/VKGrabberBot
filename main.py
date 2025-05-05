import json
import time

from VKGrabber import VKGrabber
from telegramBot import ObserverBot

with open('parameters.json') as file:
    parametersDict = json.load(file)

VKCollector = VKGrabber(parametersDict['VKToken'])
telegramBot = ObserverBot(parametersDict['botKey'], parametersDict['channelUsername'])

postList = VKCollector.GetPostFromWall(parametersDict['VKGroupID'], 10)
telegramBot.SendPost(postList)

time.sleep(1)