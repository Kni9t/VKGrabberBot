import json
import logging
from datetime import datetime

from VKGrabber import VKGrabber
from telegramBot import ObserverBot
from timeController import TimeController

with open('params/parameters.json') as file:
    parametersDict = json.load(file)
    
with open(parametersDict['groupListFileName']) as file:
   groupList = list(json.load(file))

VKCollector = VKGrabber(parametersDict['VKToken'])
telegramBot = ObserverBot(parametersDict['botKey'], parametersDict['hashFileName'])
TC = TimeController()

logging.basicConfig(
    filename = f'logs/Running_logs-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log',
    level = logging.INFO,
    format = '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    encoding='utf-8'
)

try:
    pass
    for groupID in groupList:
        telegramBot.SendPost(VKCollector.GetPostFromWall(groupID, 5), parametersDict['channelUsername'])
except Exception as e:
    print(f'Ошибка: {e}')