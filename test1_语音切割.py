import os
import time

import uuid

from pydub import AudioSegment
from pydub.silence import split_on_silence

audio = AudioSegment.from_mp3("01.wav")
loudness = audio.dBFS
audio.set_frame_rate(16000)
audio.set_channels(1)
chunks = split_on_silence(audio,
                          # must be silent for at least half a second,沉默半秒
                          min_silence_len=500,

                          # consider it silent if quieter than -16 dBFS
                          silence_thresh=-45,
                          keep_silence=400

                          )

# for i, chunk in enumerate(chunks):
#     chunk.export("%d_%s.wav" % (i, str(round(chunk.duration_seconds, 3))), format="s16le")
#     # print(i)
request = []
dirName = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
os.makedirs(dirName)  # 创建路径
for i, chunk in enumerate(chunks):
    name = "%s/%d.wav" % (dirName, i)
    chunk = chunk.set_frame_rate(16000).set_channels(1)  # 设置声道和采样率
    chunk.export(name, format='wav', codec='pcm_s16le')
    request.append([name, round(chunk.duration_seconds, 3)])
