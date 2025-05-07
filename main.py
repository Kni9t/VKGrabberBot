import json
import logging
from datetime import datetime

from VKGrabber import VKGrabber
from telegramBot import ObserverBot
from timeController import TimeController

groupList = ['hlorkens']

with open('parameters.json') as file:
    parametersDict = json.load(file)

VKCollector = VKGrabber(parametersDict['VKToken'])
telegramBot = ObserverBot(parametersDict['botKey'])
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
        telegramBot.SendPost(VKCollector.GetPostFromWall(groupID, 5), groupID)
except Exception as e:
    print(f'Ошибка: {e}')