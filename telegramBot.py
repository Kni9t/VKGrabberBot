import telebot
from telebot import types
import requests
import time
import hashlib
import json

class ObserverBot:
    def __init__(self, botkey, channelName):
        self.bot = telebot.TeleBot(botkey)
        self.channelName = channelName
        
    def generateContentHash(self, caption, url = ''):
        data = (caption or '') + str(url)
        return hashlib.md5(data.encode()).hexdigest()
        
    def SendPost(self, posts):
        if (type(posts) is list):
            posts = reversed(posts)
            
        try:
            with open('sent_posts.json', 'r') as f:
                sent_posts = list(json.load(f))
                f.close()
        except:
            sent_posts = []
        
        try:
            for post in posts:
                media_group = []
                music_group = []
                doc_group = []
                poll_group = []
                gif_group = []
                
                if (self.generateContentHash(post['text'], post['mediaLinks']) in sent_posts):
                    print(f'Пост ({post['text'][:40]}) уже опубликован!')
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
                        self.bot.send_media_group(chat_id = self.channelName, media = media_group)
                    else:
                        self.bot.send_media_group(chat_id = self.channelName, media = media_group)
                        self.bot.send_message(chat_id = self.channelName, text = post['text'])
                else:
                    if (post['text'] != ''): self.bot.send_message(chat_id = self.channelName, text = post['text'])
                    
                if (len(gif_group) > 0):
                    bif_buf_group = []
                    for gif in gif_group:
                        bif_buf_group.append(types.InputMediaDocument(media = gif['content']))
                    
                    self.bot.send_media_group(chat_id = self.channelName, media = bif_buf_group)
                    
                if (len(music_group) > 0):
                    for music in music_group:
                        self.bot.send_audio(chat_id = self.channelName,
                                            audio = requests.get(music['content']).content,
                                            title = music['title'],
                                            performer = music['artist'])
                        
                if (len(doc_group) > 0):
                    for doc in doc_group:
                        self.bot.send_document(chat_id = self.channelName, document = doc['content'])
                        
                if (len(poll_group) > 0):
                    self.bot.send_poll(
                        chat_id = self.channelName,
                        question = poll_group[0]['question'],
                        options = poll_group[0]['answers'],
                        is_anonymous = True
                    )
                
                sent_posts.append(self.generateContentHash(post['text'], post['mediaLinks']))
                time.sleep(6)
                
            with open('sent_posts.json', 'w', encoding='utf-8') as f:
                json.dump(sent_posts, f)
                f.close()
                
        except Exception as e:
            print(f'Ошибка: {e}')
            with open('sent_posts.json', 'w', encoding='utf-8') as f:
                json.dump(sent_posts, f)
                f.close()