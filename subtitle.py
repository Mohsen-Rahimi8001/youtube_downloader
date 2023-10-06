from datetime import timedelta
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled


def get_youtube_subtitle(url:str) -> str:
    """
    :param url: video page url
    :return: Content prepared for saving in subtitle_name.srt file
    """
    try:
        url = url.split('watch?v=')[1]
        subtitle_api = YouTubeTranscriptApi.get_transcript(video_id=url)
    
    except IndexError:
        url = url.split('/')[-1]
        subtitle_api = YouTubeTranscriptApi.get_transcript(video_id=url)
    
    except TranscriptsDisabled:
        return ''
    
    except Exception as err:
        raise err

    result = ''

    start_tm = timedelta(seconds=subtitle_api[0]['start'])
    end_tm = timedelta(seconds=subtitle_api[0]['duration'] + subtitle_api[0]['start'])
    text = subtitle_api[0]['text']

    counter = 1

    for chunk in subtitle_api[1:]:
        if end_tm > timedelta(seconds=chunk['start']):
            text += ' ' + chunk['text']
        else:
            result += f'{counter}\n{str(start_tm).split(".")[0]} --> {str(end_tm).split(".")[0]}\n{text}\n\n'
            counter += 1
            start_tm = timedelta(seconds=chunk['start'])
            end_tm = start_tm + timedelta(seconds=chunk['duration'])
            text = chunk['text']

    return result
