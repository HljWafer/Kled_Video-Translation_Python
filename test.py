import json
import os
import time
import uuid

from pydub.effects import speedup
from requests import get
from moviepy.editor import *
from os import path
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

# 音轨提取
from dev.wafer.kelie.test1_语音合成_百度云 import wafer_tts
from dev.wafer.kelie.test1_语音转文字_百度云 import englishVoice2Text4Baidu


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
    text = englishVoice2Text4Baidu(file)
    return text


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


# 1:视频拆分成语音和视频,
# 2:语音分段,并记录时间,
# 3:语音转文字,
# 4:翻译.英->中,
# 5:文字转语音,
# 6:对应时间做整条音频,
# 7:新音频与视频合并.
mp4Path = "09.mp4"
dirName = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
# dirName = '20191113185953'
os.makedirs(dirName)  # 创建路径
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
            ttsPathi = wafer_tts(text_cn, 5, ttsPath + str(idx) + ".mp3")
            ttsList.append([ttsPathi, fileName, min])
print(ttsList)
allpath = StitchingAudio(ttsList, dirName + "/all.wav")
#
videoclip2 = video.set_audio(AudioFileClip(allpath))
videoclip2.write_videofile(dirName + "/save.mp4")
videoclip2.close()
video.close()
print("最终合成")
# text = englishVoice2Text("01.wav")
# print(text)
