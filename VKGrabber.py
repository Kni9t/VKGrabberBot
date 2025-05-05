import requests
import json
import vk

class VKGrabber:
    def __init__(self, tokenFileName):
        gettingToken = open(tokenFileName, 'r').read().split('&')
        self.token = gettingToken[0]
        self.token_v = gettingToken[1][2:]
        
    def GetPostFromWall(self, domain, count = 1):
        postList = []
        wall = vk.API(access_token = self.token, v = self.token_v).wall.get(domain = domain, count = count)
        
        for post in wall['items']:
            bufPostDate = {}
            bufAttachmentsList = []
            
            bufPostDate['text'] = post['text']
            
            for pict in post['attachments']:
                if (pict['type'] == 'photo'):
                    bufAttachmentsList.append(pict['photo']['orig_photo']['url'])
            bufPostDate['photos'] = bufAttachmentsList
                
        return bufPostDate