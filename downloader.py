import time
from requests import get
import os
import utils
import threading


class Downloader:

    def __init__(self, url):
        self.url = url
        self.cancel : bool = False
        self.complete : bool = False
        self.pause : bool = False
        self.taken_part : int = 0

        try:
            self.content = get(url=self.url, stream=True)
            self.size = int(self.content.headers.get('content-length'))
        except Exception as e:
            print("Error in get the data stream.")
            print(f"Error message: \n{str(e)}")

    def update_progress_bar(self):
        last_value = self.taken_part
        while not self.complete:
            time.sleep(1)

            speed = (self.taken_part - last_value) / 1024
            suffix = "KBps"
            
            if speed > 1000:
                speed /= 1024
                suffix = "MBps"

            utils.print_progress_bar(self.taken_part, self.size, suffix=f"{round(speed, 2)} KBps")
            
            last_value = self.taken_part
            
    def start_download(self, res_path: str):
        if os.path.exists(res_path):
            raise FileExistsError(f"{res_path} already exists.")

        dirname = os.path.dirname(res_path)
        if not os.path.isdir(dirname):
            raise FileNotFoundError(f"{dirname} directory is not valid.")
         
        start = time.time()

        self.taken_part = 0

        try:
            chunk_size = 128

            with open(f'{res_path}', 'wb') as f:
                
                clock_thread = threading.Thread(target=self.update_progress_bar)
                clock_thread.start()
                for i, item in enumerate(self.content.iter_content(chunk_size=chunk_size)):
                    while self.pause:
                        pass

                    if self.cancel:
                        return

                    f.write(item)

                    self.taken_part += len(item)

            self.complete = True
            clock_thread.join()
        
        except Exception as err:
            raise err

        print(f'\ntime spent downloading : {round(time.time() - start, 2)} seconds')

    def cancel_download(self):
        self.cancel = True

    def pause_download(self):
        self.pause = True

    def play_download(self):
        self.pause = False
