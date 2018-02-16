# -*- coding: utf-8 -*-
#マイク0番からの入力を受ける。一定時間(RECROD_SECONDS)だけ録音し、ファイル名：mono.wavで保存する。
 
import pyaudio
import sys
import time
import wave
import requests
import os
import json

def recognize():
    url = "https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY={}".format(APIKEY)
    files = {"a": open(PATH, 'rb'), "v":"on"}
    r = requests.post(url, files=files)
    if r.status_code == 401:
        message = "#$&%"
    else: message = r.json()['text']
    print 'You: '+message
    return message
    
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
    if message != "#$&%":
        r = requests.post(url, data=json.dumps(payload))
        print r.json()['utt']
        return r.json()['utt']
    else:
        print 'Lovie: すみません、よく聞き取れませんでした'
        return "すみません、よく聞き取れませんでした"

def talk(message="こんにちは", card=1, device=0):
    os.system('/home/pi/aquestalkpi/AquesTalkPi " ' + message + ' " | aplay')

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
 
if __name__ == '__main__':
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    PATH = 'output.wav'
    APIKEY='6b33652f5a637343696f2f6e79703544734a456f72326f4165435961647264433576734448735579537041' #DocomoAPI Key
    CARD = 1 #OUTPUTの指定
    DEVICE = 0 #OUTPUTの指定
    
    #サンプリングレート、マイク性能に依存
    RATE = 16000
    #録音時間
    RECORD_SECONDS = 5
    
    while 1:
        record()
        message = recognize()
        if message == "さようなら":
            break
        talk_message = dialogue(message)
        talk(talk_message, CARD, DEVICE)
