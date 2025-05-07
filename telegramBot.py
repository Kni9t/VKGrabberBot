import telebot
from telebot import types
import requests
import time
import hashlib
import json
import logging

class ObserverBot:
    def __init__(self, botkey, hashFileName = 'sent_posts.json', adminId = None):
        self.bot = telebot.TeleBot(botkey)
        self.hashFileName = hashFileName
        self.backupHashFileName = 'backupHash.json'
        self.adminId = adminId
        
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f'ObserverBot успешно создан!')
        self.SendMsgToAdmin('Бот для парсинга постов из VK был успешно инициирован! Вы были указаны как администратор. В случае критических ошибок бота, Вам будет направлено уведомление!')
        
    def generateContentHash(self, caption, url = ''):
        data = (caption or '') + str(url)
        return hashlib.md5(data.encode()).hexdigest()
    
    def resizeText(self, text):
        resultTextList = []
        
        if (len(text) > 4096):
            bufStr = ''
            for paragraph in text.split('\n'):
                if (len(bufStr) + len(paragraph) > 4095):
                    resultTextList.append(bufStr)
                    bufStr = paragraph
                else:
                    bufStr += ('\n' + paragraph)
                    
            resultTextList.append(bufStr)
        else:
            resultTextList = [text]
        
        return resultTextList
    
    def SendStr(self, str, channelName):
        try:
            bufStr = self.resizeText(str)
        
            for message in bufStr:
                self.bot.send_message(chat_id = channelName, text = message)
                
            self.logger.debug(f'Сообщение ({message[:20].replace('\n', '')}) в канал: {channelName}')
        except Exception as e:
            msg = f'В SendStr произошла ошибка отправления сообщения: ({message[:20].replace('\n', '')}) в канал: {channelName} - {e}'
            print(msg)
            self.logger.error(msg)
    
    def SendMsgToAdmin(self, str):
        if (self.adminId is not None):
            try:
                self.bot.send_message(chat_id = self.adminId, text = str)
                    
                self.logger.debug(f'Сообщение ({str}) отправлено администратору {self.adminId}')
            except Exception as e:
                msg = f'Ошибка оповещения администратора: {self.adminId}! - {e}'
                print(msg)
                self.logger.error(msg)
         
    def SaveHashs(self, hash):
        try:
            with open(self.hashFileName, 'w', encoding='utf-8') as file:
                json.dump(hash, file)
                file.close()
                
                self.logger.debug(f'Hash успешно сохранены в файл {self.hashFileName}!')
        except Exception as e:
            msg = f'Ошибка сохранения hash в файл: {self.hashFileName}!\n{e}\nПопытка сохранить данные в резервный файл {self.backupHashFileName}...'
            
            self.SendMsgToAdmin(msg)
            
            print(msg)
            self.logger.error(msg)
            
            try:
                with open(self.backupHashFileName, 'w', encoding='utf-8') as file:
                    json.dump(hash, file)
                    file.close()
                    
                    self.logger.debug(f'Hash успешно сохранены в резервный файл {self.backupHashFileName}!')
            except Exception as ex:
                msg = f'Ошибка сохранения hash в резервный файл {self.backupHashFileName}! Данные для Hash файла потеряны!\n{ex}'
                
                self.SendMsgToAdmin(msg)
                
                print(msg)
                self.logger.error(msg)
    
    def LoadHash(self):
        result = []
        try:
            with open(self.hashFileName, 'r') as file:
                result = list(json.load(file))
                file.close()
                
                self.logger.debug(f'Hash файл {self.hashFileName} успешно загружен!')
        except Exception as e:
            msg = f'Ошибка загрузки данных из файла: {self.hashFileName}!\n{e}\nБудет создан новый файл hash!'
            
            self.SendMsgToAdmin(msg)
            
            print(msg)
            self.logger.error(msg)
        return result
        
    def SendPost(self, posts, channelName):
        sent_posts = self.LoadHash()
        
        if (len(posts) == 0):
            msg = f'Не найдено постов для отправки!'
                    
            print(msg)
            self.logger.info(msg)
        
        if (type(posts) is list):
            posts = reversed(posts)
        
        for post in posts:
            try:
                media_group = []
                music_group = []
                doc_group = []
                poll_group = []
                gif_group = []
                
                if (self.generateContentHash(post['text'], post['mediaLinks']) in sent_posts):
                    msg = f'Пост ({self.generateContentHash(post['text'], post['mediaLinks'])}) из {post['groupName']} уже опубликован!'
                    
                    print(msg)
                    self.logger.info(msg)
                    continue
                
                for mediaLink in post['mediaLinks']:
                    if ((mediaLink['type'] == 'photo') or (mediaLink['type'] == 'video')):
                        media_group.append(types.InputMediaPhoto(mediaLink['content']))
                    
                    if (mediaLink['type'] == 'gif'):
                        if (len(media_group) == 0):
                            media_group.append(types.InputMediaDocument(media = mediaLink['content']))
                        else:
                            gif_group.append(mediaLink)
                    
                    if (mediaLink['type'] == 'doc'):
                        doc_group.append(mediaLink)
                        
                    if (mediaLink['type'] == 'audio'):
                        music_group.append(mediaLink)
                        
                    if (mediaLink['type'] == 'poll'):
                        poll_group.append(mediaLink)
                        
                if (len(media_group) > 0):
                    if (len(post['text']) <= 1024):
                        media_group[0].caption = post['text']
                        self.bot.send_media_group(chat_id = channelName, media = media_group)
                    else:
                        self.bot.send_media_group(chat_id = channelName, media = media_group)
                        if (post['text'] != ''): self.SendStr(post['text'], channelName)
                else:
                    if (post['text'] != ''): self.SendStr(post['text'], channelName)
                    
                if (len(gif_group) > 0):
                    bif_buf_group = []
                    for gif in gif_group:
                        bif_buf_group.append(types.InputMediaDocument(media = gif['content']))
                    
                    self.bot.send_media_group(chat_id = channelName, media = bif_buf_group)
                    
                if (len(music_group) > 0):
                    for music in music_group:
                        self.bot.send_audio(chat_id = channelName,
                                            audio = requests.get(music['content']).content,
                                            title = music['title'],
                                            performer = music['artist'])
                        
                if (len(doc_group) > 0):
                    for doc in doc_group:
                        self.bot.send_document(chat_id = channelName, document = doc['content'])
                        
                if (len(poll_group) > 0):
                    self.bot.send_poll(
                        chat_id = channelName,
                        question = poll_group[0]['question'],
                        options = poll_group[0]['answers'],
                        is_anonymous = True
                    )
                
                sent_posts.append(self.generateContentHash(post['text'], post['mediaLinks']))
                self.SaveHashs(sent_posts)
                
                msg = f'Пост ({self.generateContentHash(post['text'], post['mediaLinks'])}) из {post['groupName']} успешно опубликован!'
                    
                print(msg)
                self.logger.info(msg)
                
                time.sleep(6)
                
            except Exception as e:
                msg = f'При отправке поста произошла ошибка: {e}'
                
                self.SendMsgToAdmin(msg)
                        
                print(msg)
                self.logger.error(msg)
                
                self.SaveHashs(sent_posts)