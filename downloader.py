import requests
from tqdm import tqdm
import os

def download(url:str, filePath:str,  header:dict, session:requests.Session, chunk_size=8192):
    if not os.path.exists(filePath):
        print("Path does not exist! Crate the path %s and then try again"%(os.path.dirname(filePath)))
        exit()
    try:
        session.headers.update(header)
        response = session.get(url, headers=header, stream=True)
        response.raise_for_status()  # Check if the request was successful
        total_size = int(response.headers.get('content-length', 0))
        with open(filePath, 'wb') as file, tqdm(
                desc=filePath,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as progress_bar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                file.write(chunk)
                progress_bar.update(len(chunk))
    except FileNotFoundError:
        os.mkdir('videos')
        download(url, filePath, header, session)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
