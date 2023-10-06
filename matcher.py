import moviepy.editor as mpe
import os

def matcher(video_path, audio_path, result_path):
    """
    matches audio and video
    """
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"{video_path} is not a valid file path.")

    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"{audio_path} is not a valid file path.")

    audio = mpe.AudioFileClip(audio_url)
    video = mpe.VideoFileClip(video_url)
    final = video.set_audio(audio)
    final.write_videofile(result_path, codec='libx264', audio_codec='libvorbis')
