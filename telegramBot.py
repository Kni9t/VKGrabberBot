import telebot
from telebot import types
import requests

class ObserverBot:
    def __init__(self, botkey, channelName):
        self.bot = telebot.TeleBot(botkey)
        self.channelName = channelName
        
    def SendPost(self, posts):
        if (type(posts) is list):
            posts = reversed(posts)
        
        for post in posts:
            media_group = []
            music_group = []
            doc_group = []
                
            for mediaLink in post['mediaLinks']:
                if ((mediaLink['type'] == 'photo') or (mediaLink['type'] == 'video')):
                    media_group.append(types.InputMediaPhoto(mediaLink['content']))
                
                if (mediaLink['type'] == 'gif'):
                    media_group.append(types.InputMediaDocument(media = mediaLink['content']))
                
                if (mediaLink['type'] == 'doc'):
                    doc_group.append(mediaLink)
                    
                if (mediaLink['type'] == 'audio'):
                    music_group.append(mediaLink)
                    
            if (len(media_group) > 0):
                if (len(post['text']) <= 1024):
                    media_group[0].caption = post['text']
                    self.bot.send_media_group(chat_id = self.channelName, media = media_group)
                else:
                    self.bot.send_media_group(chat_id = self.channelName, media = media_group)
                    self.bot.send_message(chat_id = self.channelName, text = post['text'])
            else:
                self.bot.send_message(chat_id = self.channelName, text = post['text'])
                
            if (len(music_group) > 0):
                for music in music_group:
                    self.bot.send_audio(chat_id = self.channelName,
                                        audio = requests.get(music['content']).content,
                                        title = music['title'],
                                        performer = music['artist'])
                    
            if (len(doc_group) > 0):
                for doc in doc_group:
                    self.bot.send_document(chat_id = self.channelName, document = doc['content'])