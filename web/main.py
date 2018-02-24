# coding: utf-8
import requests
import json
import time
import socket
import sqlite3
from sound import record,talk
from speech_api import recognize_speech_from_wav
from text_analysis import tokenize
import RPi.GPIO as GPIO

INTAVAL = 3
SLEEPTIME = 3
SENSOR_PIN = 18
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)
st = time.time()-INTAVAL
CARD = 1 #音声OUTPUTの指定
DEVICE = 0 #音声OUTPUTの指定
HOST = '127.0.0.1'
PORT = 5000
slack_url = 'https://hooks.slack.com/services/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'

def send_msg(conn,name,msg):
    conn.send(name+":"+msg)
    print msg

if __name__ == '__main__':
    #DB接続
    db_conn = sqlite3.connect("data.db")
    db_cur = db_conn.cursor()
    #ソケット通信
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    s_conn, addr = s.accept()
    print 'Connected by', addr
    
    while True:
        reflesh_flg = 0
        time.sleep(1)
        ###フェーズ1：人感センサーをトリガーにして、受付を開始する
        while reflesh_flg==0:
            if(GPIO.input(SENSOR_PIN) == GPIO.HIGH) and (st + INTAVAL < time.time()):
                st = time.time()
                print("人を感知しました")
                talk_message = "カラビナテクノロジーへようこそ！どなたとのご約束ですか？"
                send_msg(s_conn,"machine",talk_message)
                talk(talk_message, CARD, DEVICE)
                break
            time.sleep(SLEEPTIME)

        ###フェーズ2：誰との約束かを特定する
        roop_cnt = 0
        while reflesh_flg==0:    
            roop_cnt += 1
            if roop_cnt >= 3:
                send_msg(s_conn,"machine","0")###画面初期化
                reflesh_flg = 1
                break

            record()
            txt = recognize_speech_from_wav()
            if txt == -1:
                talk_message =  "すみません、もう一度おねがいします"
                send_msg(s_conn,"machine",talk_message)
                talk(talk_message, CARD, DEVICE)
            else:
                send_msg(s_conn,"guest",txt)
                time.sleep(1)
                txt = tokenize(txt)
                to_name = False
                for word in txt:
                    db_cur.execute("select name,department from member where yomigana ='%s'" % word)
                    for row in db_cur:
                        to_name = row[0].encode("utf-8")
                        department = row[1].encode("utf-8")
                if to_name != False:
                    talk_message = department + "の" +to_name + "ですね。所属とお名前を教えてください。"
                    send_msg(s_conn,"machine",talk_message)
                    talk(talk_message, CARD, DEVICE)
                    break
                else:
                    talk_message =  "社員名簿にない名前です。すみません、もう一度おねがいします"
                    send_msg(s_conn,"machine",talk_message)
                    talk(talk_message, CARD, DEVICE)

        ###フェーズ3：フェーズ2で特定した社員に来客を通知する
        roop_cnt = 0
        while reflesh_flg == 0:          
            roop_cnt += 1
            if roop_cnt >= 3:
                send_msg(s_conn,"machine","0")###画面初期化
                reflesh_flg = 1
                break
            
            record()
            txt = recognize_speech_from_wav()
            if txt == -1:
                talk_message =  "すみません、もう一度おねがいします"
                send_msg(s_conn,"machine",talk_message)
                talk(talk_message, CARD, DEVICE)
            else:
                send_msg(s_conn,"guest",txt)
                time.sleep(1)
                from_name = txt
                requests.post(slack_url,data = json.dumps({'text':to_name + 'さん、' + from_name + '様がお見えになりました。'}))

                talk_message = from_name + "さま、" + to_name + "にメッセージをおくりました。少々お待ちください。"
                send_msg(s_conn,"machine",talk_message)
                talk(talk_message, CARD, DEVICE)
                time.sleep(10)
                send_msg(s_conn,"machine","0")###画面初期化
                break
