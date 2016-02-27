# -*- coding: utf-8 -*-

import motor
from torpc.server import RPCTCPServer
from torpc.client import RPCClient
from tornado import gen
from tornado.ioloop import IOLoop 
import tornado.web

from json import dumps

class RPCServerHandler(RPCTCPServer):
    db = motor.MotorClient().test

    def add(self, a, b):
        return a + b

    @gen.coroutine
    def find(self, table_name):
        res = None
        if table_name:
            res = yield self.db[table_name].find_one({}, {'_id': 0})
        raise gen.Return(res)


class RPCClientHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, func_name):
        if func_name:
            args = dict()
            if func_name == 'add':
                for arg in ("a", "b"):
                    val = self.get_argument(arg, None)
                    if val :
                        args[arg] = int(val)
            elif func_name == 'find':
                args = {'table_name': self.get_argument('table_name', '')}
            RPC_client = RPCClient()
            try:
                yield RPC_client.connect('127.0.0.1', 8890)
                res = yield RPC_client.remote_call(func_name, **args)
                self.finish(dumps(res))
            except Exception, e:
                print e

if __name__ == "__main__":
    server_app = tornado.web.Application([
            (r'/(.*)', RPCClientHandler)
            ])

    print 'Listening on http://localhost:8889'
    server_app.listen(8889)
    server = RPCServerHandler()    
    server.listen(8890)   
    IOLoop.instance().start()