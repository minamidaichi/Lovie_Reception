# coding:UTF-8
import sys
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import socket
import time
from flask import Flask, request, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/echo')
def echo():
    HOST = '127.0.0.1'    # The remote host
    PORT = 5000 # The same port as used by the server
    app_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    app_s.connect((HOST, PORT))
    
    if request.environ.get('wsgi.websocket'):
        web_s = request.environ['wsgi.websocket']
        while True:
            data = app_s.recv(1024)
            print "recive:"+data
            name = data.split(":")[0]
            msg = data.split(":")[1]
            send_data = {"name":name,"message":msg}
            web_s.send(json.dumps(send_data))
    return

if __name__ == '__main__':
    
    app.debug = True
    server = pywsgi.WSGIServer(('127.0.0.1', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()
