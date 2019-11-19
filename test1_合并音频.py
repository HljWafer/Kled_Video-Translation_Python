# from googletrans import Translator
#
# translate = Translator()
# result = translate.translate('hello', dest='zh-CN')
# print(result.text)
# 加载MP3文件
from pydub import AudioSegment

llis = [['20191112103341/tts/0.mp3', 3.013], ['20191112103341/tts/1.mp3', 4.124], ['20191112103341/tts/2.mp3', 15.996],
        ['20191112103341/tts/3.mp3', 5.546], ['20191112103341/tts/4.mp3', 13.959], ['20191112103341/tts/5.mp3', 9.277],
        ['20191112103341/tts/6.mp3', 8.251]]
llis2 = []
llis3 = []
# lll = 6153
# all = AudioSegment.empty()
# for [i, time] in llis:
#     song = AudioSegment.from_mp3(i)
#     silentt = AudioSegment.silent(duration=(time - song.duration_seconds) * 1000)
#     all += song
#     all += silentt
#
# all.export("all.mp3", format="mp3")  # 导出为MP3格式

a = AudioSegment.from_mp3("20191112193506/tts/1.mp3")
# a = AudioSegment.from_mp3("20191112152313/tts/6.mp3")
print(a)

