import argparse
from requests import Session
from video import Video
from error import *


class ThreadsDownload(Video):
    def __init__(self, url, outputPath=None):
        self.checkUrl(url)
        super().__init__(url, outputPath, Session())
    
    def checkUrl(self, url):
        if 'www.threads.net' not in url:
            raise UrlError("Url is not valid", url)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Threads Video Downloader is a python app for downloading Mats's new Threads app videos")
    parser.add_argument('-d', '--download', action='store_true', help="Download option")
    parser.add_argument('--url', '-u', required=True, help="URL argument")
    parser.add_argument('--output', '-o', help="Output path *optional by default ./videos/file name.ext")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_arguments()

    # Check if the download option is specified
    if args.url:

        if args.download:
            if args.output:
                video = ThreadsDownload(args.url, args.output)
            else:
                video = ThreadsDownload(args.url)
            video.download()
        else:
            video = ThreadsDownload(args.url)
            print(video.checkStatus())
    else:
        print("Give url, for help -h or --help")
    
    
    