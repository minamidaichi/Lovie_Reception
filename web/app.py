# coding:UTF-8
import sys
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import time
from flask import Flask, request, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/echo')
def echo():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        past_mes = ""
        while True:
            m = open("message.txt","r")
            time.sleep(2)
            for txt in m:
                if txt != past_mes:
                    #send_data = '{"name":"machine","message":"test"}'
                    name = txt.split(":")[0]
                    msg = txt.split(":")[1]
                    send_data = {"name":name,"message":msg}
                    print json.dumps(send_data)
                    ws.send(json.dumps(send_data))
                    past_mes = txt
    return

if __name__ == '__main__':
    app.debug = True
    server = pywsgi.WSGIServer(('127.0.0.1', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()

"""
f = open("./index.html");
content = f.read()
f.close()

def app(environ, start_response):
    if environ["PATH_INFO"] == '/echo':
        ws = environ["wsgi.websocket"]
        past_mes = ""
        while True:
            m = open("message.txt","r")
            time.sleep(3)
            for txt in m:
                if txt != past_mes:
                    ws.send(unicode(txt,"utf-8"))
                    past_mes = txt
    else:
        start_response("200 OK", [
                ("Content-Type", "text/html"),
                ("Content-Length", str(len(content)))
                ])
        return iter([content])

if __name__=="__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()
"""
