#!/usr/bin/env python3

import speech_recognition as sr

# obtain path to "english.wav" in the same folder as this script
from os import path

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "01.wav")

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using Sphinx

# recognize speech using Houndify
# HOUNDIFY_CLIENT_ID = "E6gJyLwza0peaSYjgf1w9g=="
# HOUNDIFY_CLIENT_KEY = "HBfNbaeF8lqTvN-7TY4ZKmfG46XAbG5wflP0y5c3ZdiS30D11hWFEafEYONI98CXiLCxbKiW_vESP_rJbcuW-A=="
# try:
#     print(r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY))
# except sr.UnknownValueError:
#     print("Houndify could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Houndify service; {0}".format(e))


# recognize speech using Wit.ai
WIT_AI_KEY = "RBI362GX4KO2GBS34ASB25NQS7IIRGJU"  # Wit.ai keys are 32-character uppercase alphanumeric strings
try:
    print(r.recognize_wit(audio, key=WIT_AI_KEY))
except sr.UnknownValueError:
    print("Wit.ai could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Wit.ai service; {0}".format(e))


# # recognize speech using Google Speech Recognition
# try:
#     # for testing purposes, we're just using the default API key
#     # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
#     # instead of `r.recognize_google(audio)`
#     print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
# except sr.UnknownValueError:
#     print("Google Speech Recognition could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Google Speech Recognition service; {0}".format(e))
