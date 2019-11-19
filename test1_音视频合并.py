# from googletrans import Translator
#
# translate = Translator()
# result = translate.translate('hello', dest='zh-CN')
# print(result.text)
# 加载MP3文件
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment

allpath = "20191112152313/all.wav"

import moviepy.editor as mp

video = mp.VideoFileClip("01.mp4")
aa = video.set_audio(mp.AudioFileClip(allpath))
aa.write_videofile("20191112114202/save.mp4")
aa.close()
video.close()
