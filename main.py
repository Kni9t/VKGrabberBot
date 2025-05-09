import json
import logging
from datetime import datetime
import time
import sys, os

from VKGrabber import VKGrabber
from telegramBot import ObserverBot
from timeController import TimeController

# v 1.4.2

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
        parametersDict = dict(json.load(file))
        file.close()
    
    with open(parametersDict['groupListFileName']) as file:
        groupList = list(json.load(file))
        file.close()
    
    if ('adminID' in parametersDict.keys()):
        telegramBot = ObserverBot(parametersDict['botKey'], parametersDict['hashFileName'], parametersDict['adminID'])
    else:
        telegramBot = ObserverBot(parametersDict['botKey'], parametersDict['hashFileName'])
    
    VKCollector = VKGrabber(parametersDict['VKToken'], telegramBot)
        
    TC = TimeController()

except Exception as e:
    msg = f'Ошибка при инициализации бота! {e}'
    
    print(msg)
    logging.info(msg)
    
    sys.exit(1)
    
while True:
    try:
        groupID = None
        
        for groupID in groupList:
            telegramBot.SendPost(VKCollector.GetPostFromWall(groupID, 5), parametersDict['channelUsername'])
        
        secondCount, nextTime = TC.timeNextHalfHour()
        
        msg = f'Ожидаю {secondCount} сек. до: {nextTime}'
        print(msg)
        logging.info(msg)
        
        time.sleep(secondCount)
            
    except Exception as e:
        msg = f'Ошибка во время работы бота с группой: {groupID}! \n{e}'
        
        telegramBot.SendMsgToAdmin(msg)
    
        print(msg)
        logging.info(msg)