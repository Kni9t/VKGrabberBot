import logging
import time
from datetime import datetime, timedelta

class TimeController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def timeNextHalfHour(self):
        try:
            now = datetime.now()
            if (now.minute == 30):
                next_hour = now + timedelta(hours=1)
                next_time = next_hour.replace(minute=0, second=0, microsecond=0)
            else:
                if now.minute < 30:
                    next_time = now.replace(minute=30, second=0, microsecond=0)
                else:
                    next_hour = now + timedelta(hours=1)
                    next_time = next_hour.replace(minute=0, second=0, microsecond=0)
                
            sleep_seconds = int((next_time - now).total_seconds())
            
            return sleep_seconds, next_time
            
            
        except Exception as e:
            msg = f'Ошибка при попытке выполнить ожидание до {next_time}: {e}'
            
            print(msg)
            self.logger.error(msg)
            
            now = datetime.now()
            
            next_hour = now + timedelta(hours=1)
            next_time = next_hour.replace(minute=0, second=0, microsecond=0)
            
            sleep_seconds = int((next_time - now).total_seconds())
            
            return sleep_seconds, next_time