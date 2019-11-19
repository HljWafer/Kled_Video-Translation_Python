import base64
import json
from urllib.error import URLError
from urllib.parse import quote_plus
from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen

import time
from moviepy.editor import *
from pydub import AudioSegment
from pydub.effects import speedup
from pydub.silence import split_on_silence
from requests import get

# 源文件
mp4Path = "01.mp4"
# 百度key替换
API_KEY = 'xxx'
SECRET_KEY = 'xxx'


def extractAudioFile(videoFile, audioFile):
    video = VideoFileClip(videoFile)
    audio = video.audio
    audio.write_audiofile(audioFile)
    return video


# 音频断句
def splitVoice(audioFile, path):
    audio = AudioSegment.from_mp3(audioFile)
    audio.set_frame_rate(16000)
    audio.set_channels(1)
    chunks = split_on_silence(audio,
                              # must be silent for at least half a second,沉默半秒
                              min_silence_len=500,

                              # consider it silent if quieter than -16 dBFS
                              silence_thresh=-45,
                              keep_silence=400

                              )
    request = []

    for i, chunk in enumerate(chunks):
        name = "%s/%d.wav" % (path, i)
        chunk = chunk.set_frame_rate(16000).set_channels(1)  # 设置声道和采样率
        chunk.export(name, format='wav', codec='pcm_s16le')
        request.append([name, round(chunk.duration_seconds, 3)])
    print("剪切成%d份" % len(request), )
    return request


def englishVoice2Text2(file):
    token = fetch_token()
    with open(file, 'rb') as speech_file:
        speech_data = speech_file.read()

    length = len(speech_data)
    if length == 0:
        return 'file %s length read 0 bytes' % file
    speech = base64.b64encode(speech_data)
    speech = str(speech, 'utf-8')
    params = {'dev_pid': 1737,  # 代表英语
              # "lm_id" : LM_ID,    #测试自训练平台开启此项
              'format': 'wav',
              'rate': 16000,  # 采样率
              'token': token,
              'cuid': '123456PYTHON',
              'channel': 1,
              'speech': speech,
              'len': length
              }
    post_data = json.dumps(params, sort_keys=False)
    req = Request('http://vop.baidu.com/server_api', post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    f = urlopen(req)
    result_str = f.read()
    result = json.loads(result_str)
    if 'result' in result.keys():
        return result['result'][0]
    else:
        return None


def translation(text):
    getBatchImageUrl = "http://fy.iciba.com/ajax.php?a=fy&f=auto&t=auto&w=" + text
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    results = get(getBatchImageUrl, headers=headers)
    con = json.loads(results.content)
    if 'out' in con['content'].keys():
        print("翻译", text, con['content']['out'])
        return con['content']['out']
    else:
        return None


def StitchingAudio(ttsList, path):
    all = AudioSegment.empty()
    for [ttsi, rawi, time] in ttsList:
        if ttsi is None:
            song = AudioSegment.from_wav(rawi)
            all += song
        else:

            song = AudioSegment.from_mp3(ttsi)
            song = speedChange(song, time)
            all += song

    all.export(path, format="wav")
    print("导出MP3", path)
    return path  # 导出为MP3格式


def speedChange(sound, time):
    speed = sound.duration_seconds / time
    if speed > 1:
        return speedup(sound, speed)
    elif speed < 1:
        silentt = AudioSegment.silent(duration=(time - sound.duration_seconds) * 1000)
        sound += silentt
        return sound
    else:
        return sound


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request('http://openapi.baidu.com/oauth/2.0/token', post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    result_str = result_str.decode()

    # print(result_str)
    result = json.loads(result_str)
    # print(result)
    if 'access_token' in result.keys() and 'scope' in result.keys():
        return result['access_token']
    else:
        return 'MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response'


def get_tts(TEXT, SPD=6, path=""):
    # 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
    PER = 106
    # 音调，取值0-15，默认为5中语调
    PIT = 6
    # 音量，取值0-9，默认为5中音量
    VOL = 6
    # 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
    AUE = 3
    TTS_URL = 'http://tsn.baidu.com/text2audio'
    token = fetch_token()
    tex = quote_plus(TEXT)  # 此处TEXT需要两次urlencode
    params = {'tok': token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE,
              'cuid': '123456PYTHON', 'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

    data = urlencode(params)

    req = Request(TTS_URL, data.encode('utf-8'))
    try:
        f = urlopen(req)
        result_str = f.read()
    except  URLError as err:
        result_str = err.read()

    with open(path, 'wb') as of:
        of.write(result_str)
    return path


# 1:视频拆分成语音和视频,
# 2:语音分段,并记录时间,
# 3:语音转文字,
# 4:翻译.英->中,
# 5:文字转语音,
# 6:对应时间做整条音频,
# 7:新音频与视频合并.

dirName = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
os.makedirs(dirName)
video = extractAudioFile(mp4Path, dirName + "/raw.wav")
splitPath = dirName + "/split/"
os.makedirs(splitPath)
voiceList = splitVoice(dirName + "/raw.wav", splitPath)
ttsPath = dirName + "/tts/"
os.makedirs(ttsPath)  # 创建路径
ttsList = []

for idx, [fileName, min] in enumerate(voiceList):
    text = englishVoice2Text2(fileName)
    if text is None:
        ttsList.append([None, fileName, min])
    else:
        text_cn = translation(text)
        if text_cn is None:
            ttsList.append([None, fileName, min])
        else:
            ttsPathi = get_tts(text_cn, 5, ttsPath + str(idx) + ".mp3")
            ttsList.append([ttsPathi, fileName, min])
print(ttsList)
allpath = StitchingAudio(ttsList, dirName + "/all.wav")
videoclip2 = video.set_audio(AudioFileClip(allpath))
videoclip2.write_videofile(dirName + "/save.mp4")
videoclip2.close()
video.close()
print("最终合成")
