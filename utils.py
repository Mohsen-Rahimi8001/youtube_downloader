def show_link(obj):
    print('---------------------------------------------')
    print('obj is :', obj)
    print('url is :', obj.url)

def reseloution_number(string:str) -> int:
    for i in range(len(string)):
        if not (48 <= ord(string[i]) <= 57):
            return int(string[:i])

def quality_compair(lower, higher) -> bool:
    if Helpers.reseloution_number(lower.resolution) < Helpers.reseloution_number(higher.resolution):
        return True
    elif lower.resolution == higher.resolution:
        if lower.fps < higher.fps:
            return True
    else:
        return False

def get_directory(directory):
    return r''+directory

def browse_button():
    raise NotImplementedError

def video_options(video_objects:list['Stream']):
    result = []
    for vdob in video_objects:
        res = (f'{vdob.itag}-{vdob}', vdob)
        result.append(res)
    return result

def audio_options(audio_objects:list['Stream']):
    result = []
    for adob in audio_objects:
        res = (f'{adob.itag}-{adob}', adob)
        result.append(res)
    return result

def find_video_option(key, video_objects: list[tuple['Stream']]) -> 'Stream':
    result = list(filter(lambda x: str(x[1].itag) == key.split('-')[0], video_objects))[0][1]
    return result

def find_audio_option(key, audio_objects:list[tuple['Stream']]) -> 'Stream':
    result = list(filter(lambda x: str(x[1].itag) == key.split('-')[0], audio_objects))[0][1]
    return result

def get_size_in_standard_scale(size) -> str:
    size = int(size)
    KB = size / 1000
    if KB < 1000:
        return '%d KB' % int(KB)
    else:
        MB = KB / 1000
        if 1000 - MB < 30:
            GB = MB / 1000
            return '%0.3f GB' % GB
        else:
            return '%0.2f MB' % MB

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}' + " " * 20, end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print('Downloaded')

