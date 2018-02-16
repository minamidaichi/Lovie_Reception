# coding: utf-8
import requests
import os

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


