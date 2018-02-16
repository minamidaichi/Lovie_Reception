# coding: utf-8
import requests
import urllib

apikey = "a5c8f4dce8d74cec9b58fe0bb03e4f67"

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
        if response.json()["RecognitionStatus"] != "InitialSilenceTimeout" and response.json()["RecognitionStatus"] != "NoMatch":
            result = response.json()["DisplayText"]
            return result
        else:
            result = u"はてな"
            return result
    else:
        raise response.raise_for_status()
