import re
import json
import requests
from error import *

class Handler():
    def __init__(self, url:str, session:requests.Session):
        self.url = url
        self.urlJs = 'https://static.xx.fbcdn.net/rsrc.php/v3ilpL4/yp/l/en_US/-xkReGEmExM.js?_nc_x=Ij3Wp8lg5Kz'
        self.urlGraph = 'https://www.threads.net/api/graphql'
        self.session = session
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
        self.headersJs = {
            'authority': 'static.xx.fbcdn.net',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'origin': 'https://www.threads.net',
            'pragma': 'no-cache',
            'referer': 'https://www.threads.net/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        self.gaphHeader = {
            'authority': 'www.threads.net',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.threads.net',
            'pragma': 'no-cache',
            'referer': self.url,
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.199", "Google Chrome";v="114.0.5735.199"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"14.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'viewport-width': '1112',
            'x-asbd-id': '129477',
            'x-csrftoken': '',
            'x-fb-friendly-name': 'BarcelonaPostPageQuery',
        }



    def crawl(self) -> dict:
        res = self.session.get(self.url, headers=self.headersInit)
        if res.status_code != 200:
            raise StatusError("Status Error", res.status_code, res.url)
        #content = BeautifulSoup(res.content, 'html.parser')
        #formated = content.prettify()
        #self.save_res('html', formated)
        post_id = re.findall(r"\"post_id\":\"[0-9]*\"", res.text, re.MULTILINE)[0].replace("\"",'').split(":")[1]
        hsi = re.findall(r"\"hsi\":\"[0-9]+\"", res.text, re.MULTILINE)[0].replace("\"",'').split(":")[1]
        spin_r = re.findall(r"\"__spin_r\":[0-9]*", res.text, re.MULTILINE)[0].split(":")[1]
        spin_t = re.findall(r"\"__spin_t\":[0-9]*", res.text, re.MULTILINE)[0].split(":")[1]
        lsd_list  = re.findall("\[\"LSD\"?.*]", res.text, re.MULTILINE)[0]
        lsd = re.findall(r"\"token\":\"[^\"]+\"", lsd_list)[0].replace("\"",'').split(":")[1]
        X_IG_App_ID = re.findall(r"\"X-IG-App-ID\":\"[^\"]+\"", lsd_list)[0].replace("\"",'').split(":")[1]

        self.session.headers.update(self.headersJs)
        params = {
            '_nc_x': 'Ij3Wp8lg5Kz',
        }
        res = self.session.get(self.urlJs, params=params, headers=self.headersJs)
        if res.status_code != 200:
            raise StatusError("Status Error", res.status_code, res.url)
        #self.save_res('js',res.text)
        doc_id = re.findall(r'[0-9]+' ,re.findall(r"params:{id:\"[0-9]*\"", res.text, re.MULTILINE)[0])[0]
        return {
            "post_id": post_id,
            "hsi":hsi,
            "spin_r": spin_r,
            "spin_t": spin_t,
            "lsd": lsd,
            "X_IG_App_ID": X_IG_App_ID,
            "doc_id": doc_id
            }

    def graphApi(self):
        attrib = self.crawl()
        data = {
            'av': '0',
            '__user': '0',
            '__a': '1',
            '__req': '1',
            '__hs': '19556.HYP:barcelona_web_pkg.2.1..0.0',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': attrib['spin_r'],
            '__s': 'plkgph:bno7b0:at64hg',
            '__hsi': attrib['hsi'], #Not found
            '__dyn': '7xeUmwlEnwn8K2WnFw9-2i5U4e0yoW3q32360CEbo1nEhw2nVE4W0om78b87C0yE465o-cw5Mx62G3i0Bo7O2l0Fwqo31wnEfovwRwlE-U2zxe2Gew9O22362W2K0zK5o4q0GpovU1aUbodEGdwtU2ewbS1LwTwNwLw8O1pwr82gxC',
            '__csr': 'gBGijox9k00lmRxy2Lxmckwky88z1aq1-zE19U4Oex2re7E8k2ybw8ZoD6G6O8mUQ4827x-0DofU466i0tk13gN02oPA0Wo7Z08423zog24g',
            '__comet_req': '29',
            'lsd': attrib['lsd'], # x-fb-lsd
            'jazoest': '21774',
            '__spin_r': attrib['spin_r'],
            '__spin_b': 'trunk',
            '__spin_t': attrib['spin_t'],
            '__jssesw': '1',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'BarcelonaPostPageQuery',
            'variables': '{"postID": "%s"}'%(attrib['post_id']),
            'server_timestamps': 'true',
            'doc_id': attrib['doc_id'], 
        }
        header = self.gaphHeader
        header['x-fb-lsd'] =  attrib['lsd']
        header['x-ig-app-id'] =  attrib['X_IG_App_ID']
        self.session.headers.update(header)
        res = self.session.post(self.urlGraph, headers=header, data=data)
        if res.status_code == 200:
            return res.json()
        else:
            raise StatusError("Status Error", res.status_code, res.url)      

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
    


if __name__ == '__main__':
    Handler().graphApi()