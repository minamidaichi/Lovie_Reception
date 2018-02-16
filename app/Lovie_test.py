# coding: utf-8
import requests
import urllib
import json
import pyaudio
import sys
import time
import wave
import requests
import os
import json

# for azure api key
apikey = "a5c8f4dce8d74cec9b58fe0bb03e4f67"
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
PATH = 'output.wav'
CARD = 1 #OUTPUTの指定
DEVICE = 0 #OUTPUTの指定
#サンプリングレート、マイク性能に依存
RATE = 16000
#録音時間
RECORD_SECONDS = 5
slack_url = 'https://hooks.slack.com/services/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'


def record():
    #pyaudio
    p = pyaudio.PyAudio() #マイク0番を設定
    input_device_index = 0 #マイクからデータ取得
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)
    all = []
    for i in range(0, RATE / chunk * RECORD_SECONDS):
        data = stream.read(chunk)
        all.append(data)
 
    stream.close()    
    data = ''.join(all)                    
    out = wave.open(PATH,'w')
    out.setnchannels(1) #mono
    out.setsampwidth(2) #16bits
    out.setframerate(RATE)
    out.writeframes(data)
    out.close()
     
    p.terminate()

def recognize_speech_from_wav( filepath="output.wav" ):

    with open(filepath, 'rb') as infile:
        raw_data = infile.read()

    token = _authorize()
    txt =  _speech_to_text( raw_data , token, lang="ja-JP", samplerate=16000, scenarios="ulm")

    return txt

def _authorize():

    url = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Content-Length": "0",
        "Ocp-Apim-Subscription-Key": apikey
    }
    response = requests.post(url, headers=headers)

    if response.ok:
        _body = response.text
        return _body
    else:
        response.raise_for_status()

def _speech_to_text( raw_data, token, lang="ja-JP", samplerate=8000, scenarios="ulm"):

    data = raw_data
    params = {
       "language": lang,
       "format": "json",
       "request_id": "request_id_999" 
    }

    # Bing Speech API呼び出し（dictationモードを指定）
    url = "https://speech.platform.bing.com/speech/recognition/dictation/cognitiveservices/v1?" + urllib.urlencode(params)
    headers = {
       "Content-type": "audio/wav; samplerate={0}".format(samplerate),
       "Authorization": "Bearer " + token 
    }

    response = requests.post(url, data=data, headers=headers)

    if response.ok:
        # 文字化け対策のためutf-8で処理する
        response.encoding = "utf-8"
        print(response.text)
        if response.json()["RecognitionStatus"] != "InitialSilenceTimeout":
            result = response.json()["DisplayText"]
            return result
        else:
            result = "?"
    else:
        raise response.raise_for_status()

def dialogue(message="こんにちは"):    
    url = "https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY={}".format(APIKEY)
    payload = {
      "utt": message,
      "context": "",
      "nickname": "光",
      "nickname_y": "ヒカリ",
      "sex": "女",
      "bloodtype": "B",
      "birthdateY": "1997",
      "birthdateM": "5",
      "birthdateD": "30",
      "age": "16",
      "constellations": "双子座",
      "place": "東京",
      "mode": "dialog",
    }
    if message != "?":
        r = requests.post(url, data=json.dumps(payload))
        print 'Lovie: ' + r.json()['utt']
        return r.json()['utt']
    else:
        print 'Lovie: すみません、よく聞き取れませんでした'
        return "すみません、よく聞き取れませんでした"

def talk(message="こんにちは", card=1, device=0):
    os.system('/home/pi/aquestalkpi/AquesTalkPi " ' + message + ' " | aplay')

if __name__ == '__main__':
    print "ready"
    while True:    
        record()
        txt = recognize_speech_from_wav()
        print txt
        reaction_words = ["らびー","ラビー","ラブ","ラヴィ","ラビ","らび","Love","Lovie","らびィ"]
        if txt in reaction_words:
            talk_mesage = "カラビナテクノロジーへようこそ！どなたとのご約束ですか？"
            print talk_message
            talk(talk_message, CARD, DEVICE)

    while True:    
        record()
        txt = recognize_speech_from_wav()
        print txt
        reaction_words = ["らびー","ラビー","ラブ","ラヴィ","ラビ","らび","Love","Lovie","らびィ"]
        if txt in reaction_words:
            requests.post(slack_url,data = json.dumps({'text':u'test @d_minami 来客 @here'}))
            talk_mesage = txt + "にメッセージをおくりました。少々お待ちください。"
            print talk_message
            talk(talk_message, CARD, DEVICE)
