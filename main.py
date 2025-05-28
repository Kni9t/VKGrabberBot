import json
import logging
from datetime import datetime
import time
import sys, os
import signal

from VKGrabber import VKGrabber
from telegramBot import ObserverBot
from timeController import TimeController

def handle_signal(signum, frame):
    msg = f"Получен сигнал закрытия бота! - {signum} Бот завершает работу..."
    
    telegramBot.SendMsgToAdmin(msg)
    logging.info(msg)
    
    sys.exit(0)
    
signal.signal(signal.SIGINT, handle_signal)   # Ctrl+C
signal.signal(signal.SIGTERM, handle_signal)  # kill

VERSION = '1.9.3'

try:
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
    filename = f'logs/Running_logs-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log',
    level = logging.DEBUG,
    format = '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    encoding='utf-8'
    )
except Exception as e:
    print(f'Ошибка при создании логгера! {e}')
    
    sys.exit(1)
    
logging.info(f'Версия запущенного бота - v.{VERSION}')

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
    
    msg = f'Бот для парсинга постов из вк в телеграм успешно инициирован! Версия запущенного бота - {VERSION}'
    
    telegramBot.SendMsgToAdmin(msg)
    logging.info(msg)

except Exception as e:
    msg = f'Ошибка при инициализации бота! {e}'
    
    print(msg)
    logging.info(msg)
    
    sys.exit(1)
    
while True:
    try:
        groupID = None
        
        for groupID in groupList:
            posts = VKCollector.GetPostFromWall(groupID, 5)
            telegramBot.SendPost(posts, parametersDict['channelUsername'])
        
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