import uuid

API_KEY = '7Cc0MQLAXpRxNSzvAyS19pzL'
SECRET_KEY = '1I3tYrr2ikgeIMf8mf5ylvAfXIvDuiQs'
# 需要识别的文件
DEV_PID = 1737


def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


CUID = get_mac_address()
# coding=utf-8

import sys
import json
import base64
import time

IS_PY3 = sys.version_info.major == 3

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode

timer = time.perf_counter

# 文件格式
FORMAT = 'wav'  # 文件后缀只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式

# 采样率
RATE = 16000  # 固定值

ASR_URL = 'http://vop.baidu.com/server_api'


class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        result_str = err.read()
    if (IS_PY3):
        result_str = result_str.decode()

    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  TOKEN end """


def englishVoice2Text4Baidu(filePath):
    token = fetch_token()

    with open(filePath, 'rb') as speech_file:
        speech_data = speech_file.read()

    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % filePath)
    speech = base64.b64encode(speech_data)
    if (IS_PY3):
        speech = str(speech, 'utf-8')
    params = {'dev_pid': DEV_PID,
              # "lm_id" : LM_ID,    #测试自训练平台开启此项
              'format': FORMAT,
              'rate': RATE,
              'token': token,
              'cuid': CUID,
              'channel': 1,
              'speech': speech,
              'len': length
              }
    post_data = json.dumps(params, sort_keys=False)
    req = Request(ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    try:
        f = urlopen(req)
        result_str = f.read()
        result = json.loads(result_str)
        if 'result' in result.keys():
            return result['result'][0]
        else:
            return None
    except URLError as err:
        print('asr http response http code : ' + str(err))
