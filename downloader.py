import time
from math import ceil
from requests import get
import os


class Downloader:

    def __init__(self, url):
        self.url = url
        self.cancel : bool = False
        self.complete : bool = False
        self.pause : bool = False
        
        try:
            self.content = get(url=self.url, stream=True)
            self.size = int(self.content.headers.get('content-length'))
        except Exception as e:
            print("Error in get the data stream.")
            print(f"Error message: \n{str(e)}")

    def start_download(self, res_path: str):
        if os.path.exists(res_path):
            raise FileExistsError(f"{res_path} already exists.")

        dirname = os.path.dirname(res_path)
        if not os.path.isdir(dirname):
            raise FileNotFoundError(f"{dirname} directory is not valid.")
         
        start = time.time()

        try:
            chunk_size = 128
           
            with open(f'{res_path}', 'wb') as f:
                for i, item in enumerate(self.content.iter_content(chunk_size=chunk_size)):

                    while self.pause:
                        pass

                    if self.cancel:
                        return

                    f.write(item)

            self.complete = True
        
        except Exception as err:
            raise err

        print(f'\ntime spent downloading : {round(time.time() - start, 2)} seconds')

    def cancel_download(self):
        self.cancel = True

    def pause_download(self):
        self.pause = True

    def play_download(self):
        self.pause = False
