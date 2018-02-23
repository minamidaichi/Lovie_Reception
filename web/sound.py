# coding: utf-8
import pyaudio
import wave
import sys
import tty
import termios
import os

PATH = 'output.wav'
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
chunk = 1024
RECORD_SECONDS = 5

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

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

def talk(message="こんにちは", card=1, device=0):
    os.system('/home/pi/aquestalkpi/AquesTalkPi " ' + message + ' " | aplay')
