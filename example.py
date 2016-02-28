# -*- coding: utf-8 -*-

from json import dumps

from torpc.server import RPCTCPServer, private
from torpc.client import RPCClient
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from tornado.ioloop import IOLoop 
import tornado.web

class RPCServerHandler(RPCTCPServer):

    @private
    def test(self):
        print('private')

    def add(self, a, b):
        return a + b

    @gen.coroutine
    def fetch(self, url):
        client = AsyncHTTPClient()
        res = yield client.fetch(url)
        raise gen.Return(res.code)


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
            elif func_name == 'fetch':
                args = {'url': self.get_argument('url', '')}
            RPC_client = RPCClient()
            try:
                yield RPC_client.connect('127.0.0.1', 8890)
                res = yield RPC_client.remote_call(func_name, **args)
                self.finish(dumps(res))
            except Exception, e:
                print(e)

if __name__ == "__main__":
    server_app = tornado.web.Application([
            (r'/(.*)', RPCClientHandler)
            ])

    print('Listening on http://localhost:8889')
    server_app.listen(8889)
    server = RPCServerHandler()
    server.listen(8890)
    IOLoop.instance().start()