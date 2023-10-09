from pytube.streams import Stream
from pytube import YouTube
import utils
import matcher
from downloader import Downloader
from subtitle import get_youtube_subtitle
from matcher import matcher
import os


class YoutubeDl(YouTube):

    download_list : dict = {
        'video' : None,
        'audio' : None,
    }

    def __init__(self, page_link, **kwargs):
        self.page_link = page_link
        self.url = YouTube(self.page_link)
        super(YoutubeDl, self).__init__(self.page_link)

    @property
    def all(self):
        return self.url.streams.all()

    @property
    def videos(self):
        return self.url.streams.filter(type='video')

    @property
    def audios(self):
        return self.url.streams.filter(type='audio')

    @property
    def progressives(self):
        return self.url.streams.filter(progressive=True)

    def downloader(self, video_object:Stream, audio_object:Stream=None):
        if audio_object is not None:
            video_download = Downloader(video_object.url, video_object.title, 'mp4', directory)
            audio_download = Downloader(audio_object.url, audio_object.title, 'mp3', directory)
            self.download_list['video'] = video_download
            self.download_list['audio'] = audio_download
            video_download.start_download(master=master, title=const.DOWNLOAD_VIDEO_TITLE, title_grid=Grid.PROGRESS_BAR_TITLE_POSITION, progress_bar_grid=progress_bar_grid)
            audio_download.start_download(master=master, title=const.DOWNLOAD_AUDIT_TITLE, title_grid=Grid.PROGRESS_BAR_TITLE_POSITION, progress_bar_grid=progress_bar_grid)
            if video_download.complete and audio_download.complete:
                matcher(movie_url=directory+f'/{video_object.title}.mp4', sound_url=directory+f'{audio_object.title}.mp3', name=video_object.title, direct=directory)
        else:
            video_download = Downloader(video_object.url, video_object.title, 'mp4', directory)
            self.download_list['video'] = video_download
            video_download.start_download(master=master, title=const.DOWNLOAD_VIDEO_TITLE, title_grid=Grid.PROGRESS_BAR_TITLE_POSITION, progress_bar_grid=progress_bar_grid)


    def cancel_downloading(self):
        for dl in self.download_list.values():
            dl.cancel_download()

    def pause_download(self):
        for dl in self.download_list.values():
            dl.pause_download()

    def play_download(self):
        for dl in self.download_list.values():
            dl.play_download()

    def download_subtitle(self, output_path):
        context = get_youtube_subtitle(self.page_link)
        if context == "":
            Warnings.CaptionWarning(msg='This video has no caption.')
            return
        with open(f'{output_path}\\{self.url.title}.srt', 'w') as srt_file:
            srt_file.write(context)

    def get_sizes(self):
        """
        :return: video size and audio size
        """
        video_size = self.download_list['video'].size
        audio_size = self.download_list['audio'].size
        return video_size, audio_size


if __name__ == "__main__":
    youtube_url = input("url: ")
    page_obj = YoutubeDl(youtube_url)

    videos = page_obj.videos
    
    while True:
        for i, vd in enumerate(videos):
            print(f"[{i}] {vd}")

        video_choice = videos[int(input("Enter video number: "))] 
        video_dl_obj = Downloader(video_choice.url)
        print(f"The video is {video_dl_obj.size / 1000000}Mb")
        if input("Do you want to change your choice?(yes/no) ").lower() == "no":
            break

    basedir = input("Enter a path to save the video: ")
    if not os.path.isdir(basedir):
        raise FileNotFoundError(f"{basedir} doesn't exist.")

    vid_name = input("The name of the video: ")

    vid_dir = os.path.join(basedir, vid_name)
    
    video_dl_obj.start_download(vid_dir)

    final_result = vid_dir

    if input("Do you want to download subtitle?(yes/no) ").lower() == "yes":        
        content = get_youtube_subtitle(youtube_url)
        sub_dir = os.path.join(basedir, f"{vid_name}.srt")
        with open(sub_dir, "w") as f:
            f.write(content)

if __name__ == "__main__2":
    youtube_url = input("Enter the url: ")

    page_obj = YoutubeDl(youtube_url)

    audios = page_obj.audios
    videos = page_obj.videos

    print("-------------------------------VIDEOS-------------------------------")
    while True:
        for i, vd in enumerate(videos):
            print(f"[{i}] {vd}")

        video_choice = videos[int(input("Enter video number: "))] 
        video_dl_obj = Downloader(video_choice.url)
        print(f"The video is {video_dl_obj.size / 1000000}Mb")
        if input("Do you want to change your choice?(yes/no) ").lower() == "no":
            break

    print("-------------------------------AUDIOS-------------------------------")
    while True:
        for i, au in enumerate(audios):
            print(f"[{i}] {au}")

        audio_choice = audios[int(input("Enter audio number: "))]
        audio_dl_obj = Downloader(audio_choice.url)
        print(f"The audio is {video_dl_obj.size / 1000000}Mb")
        if input("Do you want to change your choice?(yes/no) ").lower() == 'no':
            break

    basedir = input("Enter a path to save the video: ")
    if not os.path.isdir(basedir):
        raise FileNotFoundError(f"{basedir} doesn't exist.")

    vid_name = input("The name of the video: ")
    aud_name = vid_name + ".mp3"

    vid_dir = os.path.join(basedir, vid_name)
    aud_dir = os.path.join(basedir, aud_name)
    
    video_dl_obj.start_download(vid_dir)
    audio_dl_obj.start_download(aud_dir)

    final_result = os.path.join(basedir, "final" + vid_name)
    matcher(vid_dir, aud_dir, final_result)

    if input("Do you want to download subtitle?(yes/no) ").lower() == "yes":        
        content = get_youtube_subtitle(youtube_url)
        sub_dir = os.path.join(basedir, f"{vid_name}.srt")
        with open(sub_dir, "w") as f:
            f.write(content)
