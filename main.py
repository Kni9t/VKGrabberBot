import json
import logging
from datetime import datetime
import sys, os

from VKGrabber import VKGrabber
from telegramBot import ObserverBot
from timeController import TimeController

try:
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
    filename = f'logs/Running_logs-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log',
    level = logging.INFO,
    format = '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    encoding='utf-8'
    )
except Exception as e:
    print(f'Ошибка при создании логгера! {e}')
    sys.exit(1)

try:
    with open('params/parameters.json') as file:
        parametersDict = json.load(file)
        file.close()
    
    with open(parametersDict['groupListFileName']) as file:
        groupList = list(json.load(file))
        file.close()
except Exception as e:
    msg = f'Ошибка при чтении файла с параметрами! {e}'
    print(msg)
    logging.info(msg)
    sys.exit(1)

VKCollector = VKGrabber(parametersDict['VKToken'])
telegramBot = ObserverBot(parametersDict['botKey'], parametersDict['hashFileName'])
TC = TimeController()


try:
    pass
    for groupID in groupList:
        telegramBot.SendPost(VKCollector.GetPostFromWall(groupID, 5), parametersDict['channelUsername'])
except Exception as e:
    print(f'Ошибка: {e}')