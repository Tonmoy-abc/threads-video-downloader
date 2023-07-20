import os
import requests
from error import *
from handler import Handler
from datetime import datetime
from urllib.parse import urlparse
from downloader import download



class Video():
    def __init__(self, url:str, session:requests.Session, savePath=None,  saveDir='./videos'):
        self.url = url
        self.saveDir = saveDir
        self.session = session
        self.savePath = savePath
        self.headers = {
            'authority': 'scontent.cdninstagram.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'range': 'bytes=0-',
            'referer': 'https://www.threads.net/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'video',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
    
    def download(self):
        handler = Handler(self.url, self.session)
        try:
            data = handler.graphApi()
        except StatusError as e:
            print("Can't download .. url:%s stats code:%s"%(e['url'],e['error_code']))
            exit()
        post = data["data"]["data"]["containing_thread"]["thread_items"][0]["post"]
        self.userName = post["user"]["username"]
        self.width = post["original_width"]
        self.height = post["original_height"]
        self.videoUrlFull = post["video_versions"][0]["url"]
        self.videoExt = self.get_file_extension(urlparse(self.videoUrlFull).path)
        self.caption = post["caption"]["text"]
        self.uploaded = post["taken_at"]
        self.likeCount = post["like_count"]
        self.replyCount = post["text_post_app_info"]["direct_reply_count"]
        
        currentTime = self.current_time()
        if self.savePath == None:
            if '/' in self.saveDir[-1]:
                self.savePath = '%s%s-%s-%s.%s'%(self.saveDir, self.userName, self.caption, currentTime, self.videoExt)
            else:
                self.savePath = '%s/%s-%s-%s.%s'%(self.saveDir, self.userName, self.caption, currentTime, self.videoExt)
        
        download(
            self.videoUrlFull,
            self.savePath,
            self.videoExt,
            self.headers,
            self.session
            )
        
    def checkStatus(self):
        handler = Handler(self.url, self.session)
        try:
            handler.graphApi()["data"]["data"]["containing_thread"]["thread_items"][0]["post"]["video_versions"][0]["url"]
            return "Ok"
        except:
            return "Error"

        
        
    @classmethod
    def current_time(cls, format_str="%Y-%m-%d_%H-%M-%S"):
        now = datetime.now()
        return now.strftime(format_str)

    @classmethod
    def get_file_extension(cls, file_path):
        _, file_extension = os.path.splitext(file_path)
        return file_extension
