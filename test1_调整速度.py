from pydub import AudioSegment
from pydub.effects import speedup

audio = AudioSegment.from_mp3("01.wav")


def speed_change(sound, speed=1.0):
    return speedup(sound, speed)


# slow_sound1 = speed_change(audio, 0.7775)
# slow_sound = speed_change(audio, 0.75)
fast_sound = speed_change(audio, 2.1)
fast_sound1 = speed_change(audio, 2.2)
fast_sound2 = speed_change(audio, 2.3)
print(fast_sound.duration_seconds)
print(fast_sound1.duration_seconds)
print(fast_sound2.duration_seconds)
