import functools
from json import dumps, loads
from struct import pack, unpack
import socket

from tornado.ioloop import IOLoop
from tornado.iostream import IOStream
from tornado import gen
from constant import *

class RPCClient(object):
    """docstring for RPCClient"""
    def __init__(self, io_loop=None):
        self._io_loop = self.io_loop = io_loop or IOLoop.current()
        self._sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        #self.sock_fd.settimeout(0.5)
        self._iostream = IOStream(self._sock_fd)
        #self.stream.set_close_callback(self.on_close)

    def check_iostream(self):
        if self._iostream is None:
            return False
        try:
            self._iostream._check_closed()
        except Exception, e:
            self._iostream = None
            return False
        else:
            return True

    @gen.coroutine
    def connect(self, host, port):
        yield self._iostream.connect((host, port))

    @gen.coroutine
    def remote_call(self, method, *args, **kw):
        info_dict = {"method": method, "args": args, "kw": kw}
        req = dumps(info_dict)
        byte_num = pack('!I', len(req))
        if self.check_iostream():
            yield self._iostream.write(byte_num + req)
            data = yield self._iostream.read_bytes(MESSAGE_BYTES)
            byte_num = unpack('!I', data)[0]
            response = yield self._iostream.read_bytes(byte_num)
            response = loads(response)
            status = response['status']
            if status in status_dict:
                raise Exception(status_dict[status])
            else:
                raise gen.Return(response['result'])
        else:
            self.handle_iostream_close()

    def __getattr__(self, name):
        return functools.partial(self.remote_call, name)

    def handle_iostream_close(self):
        pass