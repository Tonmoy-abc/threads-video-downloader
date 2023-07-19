import os
import requests
from handler import Handler
from urllib.parse import urlparse
from downloader import download
from datetime import datetime


class Video():
    def __init__(self, url:str, session:requests.Session=requests.Session()):
        self.url = url
        self.session = session
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
        data = handler.graphApi()
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
        self.savePath = './videos/%s-%s-%s.%s'%(self.userName, self.caption, currentTime, self.videoExt)
        print("All data Found")
        print("Start Downloading...")
        
        download(
            self.videoUrlFull,
            self.savePath,
            self.headers,
            self.session
            )
        
        
    @classmethod
    def current_time(cls, format_str="%Y-%m-%d_%H-%M-%S"):
        now = datetime.now()
        return now.strftime(format_str)

    @classmethod
    def get_file_extension(cls, file_path):
        _, file_extension = os.path.splitext(file_path)
        return file_extension
    
if __name__ == "__main__":
    video = Video('https://www.threads.net/@ashishchanchlani/post/CuzPRZOohOn')
    video.download()