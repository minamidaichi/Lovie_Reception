# coding: utf-8
import requests
import pyaudio
from sound import record,talk
from response import dialogue
from speech_api import recognize_speech_from_wav
from text_analysis import tokenize
import json

mes_file = open("web/message.txt","w")
mes_file.close()

def write_msg(name,msg):
    mes_file = open("web/message.txt","w")
    mes_file.write(name+":"+msg)
    mes_file.close()

if __name__ == '__main__':
    CARD = 1 #OUTPUTの指定
    DEVICE = 0 #OUTPUTの指定
    slack_url = 'https://hooks.slack.com/services/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'

    ###フェーズ1
    talk_message = "カラビナテクノロジーへようこそ！どなたとのご約束ですか？"
    write_msg("machine",talk_message)
    print talk_message
    talk(talk_message, CARD, DEVICE)

    ###フェーズ2
    while True:    
        record()
        txt = recognize_speech_from_wav()
        write_msg("guest",txt)
        txt = tokenize(txt)
        reaction_words = ["ミナミ","カワカミ"]
        matched_list = [word for word in txt if word in reaction_words]
        if len(matched_list) == 1:
            to_name = matched_list[0]
            talk_message = to_name + "ですね。所属とお名前を教えてください。"
            write_msg("machine",talk_message)
            print talk_message
            talk(talk_message, CARD, DEVICE)
            break
        else:
            talk_message =  "すみません、もう一度おねがいします"
            write_msg("machine",talk_message)
            print talk_message
            talk(talk_message, CARD, DEVICE)

    ###フェーズ3
    while True:    
        record()
        txt = recognize_speech_from_wav()
        write_msg("guest",txt)
        from_name = txt.encode("utf-8")
        requests.post(slack_url,data = json.dumps({'text':to_name + 'さん、' + from_name + '様がお見えになりました。'}))
        talk_message = from_name + "さま、" + to_name + "にメッセージをおくりました。少々お待ちください。"
        write_msg("machine",talk_message)
        print talk_message
        talk(talk_message, CARD, DEVICE)

        ###キャッシュ削除的な
        mes_file = open("web/message.txt","w")
        mes_file.close()
        break
