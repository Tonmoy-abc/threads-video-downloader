import argparse
from requests import Session
from video import Video
from error import *


class ThreadsDownload(Video):
    def __init__(self, url, outputPath=None, outputDir="./videos"):
        self.checkUrl(url)
        super().__init__(url, Session(), outputPath, outputDir)
    
    def checkUrl(self, url):
        if 'www.threads.net' not in url:
            raise UrlError("Url is not valid", url)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='app.py' , description="Threads Video Downloader is a python app for downloading Mats's new Threads app videos")
    parser.add_argument('-d', '--download', action='store_true', help="Download option")
    parser.add_argument('--url', '-u', help="URL of the video")
    parser.add_argument('--output', '-o', help="Output path *optional by default ./videos/file_name.ext")
    parser.add_argument('--input', '-i', help="Input txt file path for multiple videos download together *optional")
    parser.add_argument('--dir', help="The directory for saving files")
    args = parser.parse_args()
    return args

def get_url_form_txt(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        data = f.read().split('\n')
        f.close()
        for url in data:
            if url.strip() != '' and 'www.threads.net' in url:
                yield url

def multipleHandle(path, download):
    data = get_url_form_txt(path)
    for url in data:
        if args.dir:
            video =ThreadsDownload(url, outputDir=args.dir)
            if download:
                if args.dir:
                    video.download()
            else:
                print(url,'->',video.checkStatus())
        else:
            video =ThreadsDownload(url)
            if download:
                if args.dir:
                    video.download()
            else:
                print(url,'->',video.checkStatus())

if __name__ == "__main__":
    args = parse_arguments()
    print("Threads Download")

    if args.input:
        multipleHandle(args.input, args.download)
    elif args.url:
        if args.download:
            if args.output:
                video = ThreadsDownload(args.url, args.output)
            elif args.dir:
                video = ThreadsDownload(args.url, outputDir=args.dir)
            else:
                video = ThreadsDownload(args.url)
            video.download()
        else:
            video = ThreadsDownload(args.url)
            print(video.checkStatus())
    else:
        print("Give url, for help -h or --help")
    
    
    