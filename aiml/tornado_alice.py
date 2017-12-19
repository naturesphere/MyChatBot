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
import aiml

logging.basicConfig(level=logging.INFO)

class MainHandler(tornado.web.RequestHandler):

    def retriveInput(self):
        reString = '{ "result": 0, "response": ":-)"}'
        global kernel
        try:
            key = self.get_argument('key').strip()
            lang = self.get_argument('lang').strip()
            inpt = self.get_argument('input').strip()
            if key=="xxxx" and lang=="en" and inpt:
                response = kernel.respond(inpt)     
                if response.strip()=="":
                    response = "I'm sorry ..."
                reString = '{"response":"'+str(response)+'"' + ',"id":88888888,"result":100,"msg":"OK."}'
                self.write(reString)
                # try:    # write to mongdb
                #     # day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                #     moment = time.strftime('%H:%M:%S',time.localtime(time.time()))
                #     record = {  
                #                 'moment':moment,
                #                 'ip':self.request.remote_ip,
                #                 'question':inputKeys,
                #                 'answer':response
                #             }
                #     colletion = time.strftime('day_%Y%m%d',time.localtime(time.time())) 
                #     DB[colletion].insert_one(record)
                # except Exception as msg:
                #     print(msg)
            else:
                self.write("some thing wrong")
        except Exception as e:
            self.write("Err: %s" % e)

    def get(self):   
       self.retriveInput()

    def post(self):
        self.retriveInput()

def make_app(db):
    return tornado.web.Application([
        (r"/getreply", MainHandler),
    ],db=db)

if __name__ == "__main__":
    #parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000, help='port')
    # parser.add_argument('--modelTag', type=str, default='server', help='model suffix')
    args = parser.parse_args(sys.argv[1:])

    # chat bot
    kernel = aiml.Kernel()
    kernel.learn("startup.xml")
    kernel.respond("load aiml b")

    # mongdb client
    server_site = '127.0.0.1'
    server_port = 27017
    database = 'chatbotDB'
    DB = motor.motor_tornado.MotorClient(server_site,server_port)[database]

    #system arguments
    app = make_app(DB)
    app.listen(args.port)
    IOLoop.current().start()