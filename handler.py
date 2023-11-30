import re
import json
import requests
from error import *
from bs4 import BeautifulSoup

class Handler():
    def __init__(self, url:str, session:requests.Session, DEBUG=False):
        self.url = url
        self.urlJs = ''
        self.urlGraph = 'https://www.threads.net/api/graphql'
        self.session = session
        self.DEBUG = DEBUG
        self.headersInit = {
            'authority': 'www.threads.net',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

    def script_parser(self, html:BeautifulSoup)->dict:
        scripts = html.select("script")
        for i, script in enumerate(scripts):
            if script.string !=  None:
                if "username" in script.string and "original_width" in script.string:
                    break
        s = json.loads(script.string)
        return s["require"][0][3][0]["__bbox"]["require"][0][3][1]["__bbox"]["result"]

    def crawl(self) -> dict:
        res = self.session.get(self.url, headers=self.headersInit)
        if res.status_code != 200:
            raise StatusError("Status Error", res.status_code, res.url)
        content = BeautifulSoup(res.content, 'html.parser')
        
        if self.DEBUG:
            formated = content.prettify()
            self.save_res('html', formated)

        return self.script_parser(content)

    @classmethod
    def save_res(cls, type:str, data):
        with open(f'res.{type}', 'w', encoding='utf-8') as f:
            if type == 'html':
                f.write(data)
            elif type == 'json':
                json.dump(data, f)
            elif type == 'js':
                f.write(data)
            f.close()

if __name__ == "__main__":
    h = Handler("url ('-')", session=requests.Session(), DEBUG=True)
    h.crawl()
    print(h.crawl())