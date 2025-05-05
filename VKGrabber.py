import requests
import json
import vk

class VKGrabber:
    def __init__(self, token):
        gettingToken = token.split('&')
        self.token = gettingToken[0]
        self.token_v = gettingToken[1][2:]
        
    def GetPostFromWall(self, domain, count = 1):
        # Returns data as a list of dictionaries. Where each element describes the post and contains the text and a list of all attached photos.
        # [
        #     {
        #         'text': 'Some text for first post',
        #         'photos': ['url1', 'url2' ...],
        #         'videos': ['url1', 'url2' ...],
        #     },
        #     ...
        # ] 
        
        postList = []
        wall = vk.API(access_token = self.token, v = self.token_v).wall.get(domain = domain, count = count)
        
        for post in wall['items']:
            bufPostDate = {
                'text': None,
                'mediaLinks': None,
            }
            bufMediaList = []
            
            bufPostDate['text'] = post['text']
            
            for attach in post['attachments']:
                if (attach['type'] == 'photo'):
                    bufMediaList.append(attach['photo']['orig_photo']['url'])
                if (attach['type'] == 'video'):
                    bufMediaList.append(f'https://vk.com/video{attach['video']['owner_id']}_{attach['video']['id']}?access_key={attach['video']['access_key']}')
           
            bufPostDate['mediaLinks'] = bufMediaList
            
            postList.append(bufPostDate)
            
        return postList