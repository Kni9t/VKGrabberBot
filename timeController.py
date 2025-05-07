import logging
import time
from datetime import datetime, timedelta

class TimeController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def sleepToNextHalfHour(self):
        try:
            now = datetime.now()
    
            if (now.minute < 30):
                minute = 0 
            else:
                minute = 30
            
            next_run = now.replace(minute = minute, second=0, microsecond=0)
            
            if now >= next_run:
                next_run += timedelta(minutes = 30)
                
            sleep_seconds = int((next_run - now).total_seconds())
            
            msg = f'Ожидаю {sleep_seconds} сек. до: {next_run}'
            
            print(msg)
            self.logger.info(msg)
            time.sleep(sleep_seconds)
            
        except Exception as e:
            msg = f'Ошибка при попытке выполнить ожидание до {next_run}: {e}'
            
            print(msg)
            self.logger.error(msg)