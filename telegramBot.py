import telebot
from telebot import types

class ObserverBot:
    def __init__(self, botkey, channelName):
        self.bot = telebot.TeleBot(botkey)
        self.channelName = channelName
        
    def SendPost(self, posts):
        if (type(posts) is list):
            posts = reversed(posts)
        
        for post in posts:
            media_group = []
            longText = False
            
            if (post['photos'] != []):
                for i, link in enumerate(post['photos']):
                    if i == 0:
                        if (len(post['text']) <= 1024):
                            media = types.InputMediaPhoto(link, caption = post['text'])
                        else:
                            longText = True
                            media = types.InputMediaPhoto(link)
                    else:
                        media = types.InputMediaPhoto(link)
                    media_group.append(media)
                self.bot.send_media_group(chat_id = self.channelName, media = media_group)
                if (longText): self.bot.send_message(chat_id = self.channelName, text = post['text'])
            else:
                self.bot.send_message(chat_id = self.channelName, text = post['text'])