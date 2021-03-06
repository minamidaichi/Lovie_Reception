# coding: utf-8
import requests
import json
import time
from sound import record,talk
from response import dialogue
from speech_api import recognize_speech_from_wav
from text_analysis import tokenize

mes_file = open("web/message.txt","w")
mes_file.close()

def write_msg(name,msg):
    mes_file = open("web/message.txt","w")
    mes_file.write(name+":"+msg)
    print msg
    mes_file.close()

if __name__ == '__main__':
    CARD = 1 #音声OUTPUTの指定
    DEVICE = 0 #音声OUTPUTの指定
    slack_url = 'https://hooks.slack.com/services/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'

    while True:
        ###フェーズ1：人感センサーをトリガーにして、受付を開始する
        print "エンターで録音開始¥n"
        button = raw_input()
        talk_message = "カラビナテクノロジーへようこそ！どなたとのご約束ですか？"
        write_msg("machine",talk_message)
        talk(talk_message, CARD, DEVICE)

        ###フェーズ2：誰との約束かを特定する
        while True:    
            record()
            txt = recognize_speech_from_wav()
            if txt == -1:
                talk_message =  "すみません、もう一度おねがいします"
                write_msg("machine",talk_message)
                talk(talk_message, CARD, DEVICE)
            else:
                write_msg("guest",txt)
                time.sleep(2)
                txt = tokenize(txt)
                reaction_words = ["ミナミ","カワカミ","サギョウ"]
                matched_list = [word for word in txt if word in reaction_words]
                if len(matched_list) != 0:
                    to_name = matched_list[0]
                    talk_message = to_name + "ですね。所属とお名前を教えてください。"
                    write_msg("machine",talk_message)
                    talk(talk_message, CARD, DEVICE)
                    break
                else:
                    talk_message =  "社員名簿にない名前です。すみません、もう一度おねがいします"
                    write_msg("machine",talk_message)
                    talk(talk_message, CARD, DEVICE)

        ###フェーズ3：フェーズ2で特定した社員に来客を通知する
        while True:    
            record()
            txt = recognize_speech_from_wav()
            if txt == -1:
                talk_message =  "すみません、もう一度おねがいします"
                write_msg("machine",talk_message)
                talk(talk_message, CARD, DEVICE)
            else:
                write_msg("guest",txt)
                time.sleep(2)
                from_name = txt
                requests.post(slack_url,data = json.dumps({'text':to_name + 'さん、' + from_name + '様がお見えになりました。'}))

                talk_message = from_name + "さま、" + to_name + "にメッセージをおくりました。少々お待ちください。"
                write_msg("machine",talk_message)
                talk(talk_message, CARD, DEVICE)
                break

