#!/usr/bin/python
# -*- coding:utf-8 -*-
# http://127.0.0.1:8000/CHATBOT?apikey=b1275afe-39f6-39c4-77b4-e5328dddba7&lang=en&kw=hi 



from tornado.ioloop import IOLoop
import tornado.web
from tornado.websocket import websocket_connect
import logging
import json
import time
import threading

import motor.motor_tornado
import time
import sys
import argparse

from cleverwrap import CleverWrap

logging.basicConfig(level=logging.INFO)

class MongDBConnector():
    
    def __init__(self,server_site,server_port,database,colletion):
        self.server_site = server_site
        self.server_port = server_port
        try:
            self.colletion = MongoClient(server_site,server_port)[database][colletion]
        except Exception as msg:
            print(msg)
            self.colletion = None

    def insert_record(self, ip, question, answer):
        day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        moment = time.strftime('%H:%M:%S',time.localtime(time.time()))
        record = {  'day':day,
                    'moment':moment,
                    'ip':ip,
                    'question':question,
                    'answer':answer
                }
        self.colletion.insert_one(record)

class MainHandler(tornado.web.RequestHandler):

    def retriveInput(self):
        reString = '{ "result": 0, "response": ":-)"}'

        global DB, CW
        try:
            inputKeys = self.get_argument('kw').strip()
            langKeys = self.get_argument('lang').strip()
            apiKeys = self.get_argument('apikey').strip()
            if apiKeys == "b1275afe-39f6-39c4-77b4-e5328dddba7" and inputKeys:

                response = CW.say(inputKeys)
                reString = '{"response":"'+str(response)+'"' + ',"id":88888888,"result":100,"msg":"OK."}'

                self.write(reString)
                try:    # write to mongdb
                    # day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                    moment = time.strftime('%H:%M:%S',time.localtime(time.time()))
                    record = {  
                                'moment':moment,
                                'ip':self.request.remote_ip,
                                'question':inputKeys,
                                'answer':response
                            }
                    colletion = time.strftime('day_%Y%m%d',time.localtime(time.time())) 
                    DB[colletion].insert_one(record)
                except Exception as msg:
                    print(msg)
            else:
                self.write(reString)
        except Exception as e:
            self.write("Err: %s" % e)

    def get(self):   
       self.retriveInput()

    def post(self):
        self.retriveInput()

def make_app(db):
    return tornado.web.Application([
        (r"/CHATBOT", MainHandler),
    ],db=db)

if __name__ == "__main__":
    ##parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000, help='port')
    args = parser.parse_args(sys.argv[1:])

    # cleverbot
    CW = CleverWrap("CC5rkRh9_2fJ05hSgbaQ6DOCAig")

    # mongdb client
    server_site = '127.0.0.1'
    server_port = 27017
    database = 'CleverbotDB'
    DB = motor.motor_tornado.MotorClient(server_site,server_port)[database]

    # system arguments
    app = make_app(DB)
    app.listen(args.port)
    IOLoop.current().start()