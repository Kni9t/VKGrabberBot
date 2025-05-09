import requests
import time
import json
import vk
import logging

from telegramBot import ObserverBot

class VKGrabber:
    def __init__(self, token, telebot: ObserverBot):
        gettingToken = token.split('&')
        self.token = gettingToken[0]
        self.token_v = gettingToken[1][2:]
        
        self.bot = telebot
        self.logger = logging.getLogger(__name__)
        
    def GetPostFromWall(self, domain, count = 1):
        # Returns data as a list of dictionaries. Where each element describes the post and contains the text and a list of all attached photos.
        # [
        #     {
        #         'groupName': <group id>,
        #         'text': 'Some text for first post',
        #         'mediaLinks': [
            #                    {'type': 'photo',
            #                     'content': <url here>},
            #                    {'type': 'video',
            #                     'content': <url here>},
            #                    {'type': 'audio',
            #                     'content': <url here>,
            #                     'title': <title here>,
            #                     'artist': <artist here>},
            #                    {'type': 'poll',
            #                     'answers': <answer list here>},
            #                     'question': <str question here>}
            #                     ...],
        #     },
        #     ...
        # ]
        
        wall = []
        
        try:
            if (count > 100):
                lastCount = -1
                while (len(wall) < count) and (len(wall) != lastCount):
                    lastCount = len(wall)
                    wall += (vk.API(access_token = self.token, v = self.token_v).wall.get(domain = domain, count = 100, offset = len(wall))['items'])
                    time.sleep(6)
            else:
                wall = vk.API(access_token = self.token, v = self.token_v).wall.get(domain = domain, count = count)['items']
            
            msg = f'Успешно получено {len(wall)} постов из группы: {domain}'
            
            self.logger.info(msg)
            
        except Exception as e:
            msg = f'При выгрузке постов со стены группы: {domain} произошла ошибка: {e}'
            
            self.bot.SendMsgToAdmin(msg)
                    
            print(msg)
            self.logger.error(msg)
            return []
        
        postList = []
        
        for post in wall:
            bufPostDate = {
                'groupName': domain,
                'text': '',
                'mediaLinks': [],
            }
            bufMediaList = []
            
            bufPostDate['text'] = post['text']
            
            if('copy_history' in post.keys()):
                continue
            
            for attach in post['attachments']:
                if (attach['type'] == 'photo'):
                    bufMediaList.append({
                        'type': 'photo', 
                        'content': attach['photo']['orig_photo']['url']
                        })
                    
                if (attach['type'] == 'video'):
                    if(attach['video']['type'] == 'video'):
                        bufMediaList.append({
                            'type': 'video',
                            'content': f'https://vk.com/video{attach['video']['owner_id']}_{attach['video']['id']}?access_key={attach['video']['access_key']}'
                            })
                        
                    if(attach['video']['type'] == 'short_video'):
                        break
                    
                if (attach['type'] == 'audio'):
                    bufMediaList.append({
                        'type': 'audio', 
                        'content': attach['audio']['url'],
                        'title': attach['audio']['title'],
                        'artist': attach['audio']['artist']
                        })
                    
                if (attach['type'] == 'doc'):
                    if (attach['doc']['ext'] == 'gif'):
                        bufMediaList.append({
                            'type': 'gif', 
                            'content': attach['doc']['url']
                            })
                    else:
                        bufMediaList.append({
                            'type': 'doc', 
                            'content': attach['doc']['url']
                            })
                        
                if (attach['type'] == 'poll'):
                    bufAnswerList = []
                    for answer in attach['poll']['answers']:
                        bufAnswerList.append(answer['text'])
                        
                    bufMediaList.append({
                        'type': 'poll', 
                        'answers': bufAnswerList,
                        'question': attach['poll']['question']
                        })
           
            bufPostDate['mediaLinks'] = bufMediaList
            
            postList.append(bufPostDate)
            
            self.logger.info(f'Пост ({post['text'][:30].replace('\n', '')}) успешно получен!')
            
        return postList