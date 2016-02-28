from struct import pack, unpack
from json import dumps, loads

from tornado.tcpserver import TCPServer    
from tornado import gen
from tornado.concurrent import is_future
from constant import *

def private(f):
    f.private = True
    return f

class Connection(object):    
    clients = set()    
    def __init__(self, RPC_TCP_server, stream, address):   
        Connection.clients.add(self)
        self._server = RPC_TCP_server
        self._stream = stream
        self._address = address
        self.read_message_bytes()
        
    def read_message_bytes(self):
        self._stream.read_bytes(MESSAGE_BYTES, self.read_message)    
    
    def read_message(self, data):
        _bytes = unpack('!I', data)[0]
        self._stream.read_bytes(_bytes, self.handle_request) 

    def _done_callback(self, f):
        res = dumps(f.result())
        _bytes = pack('!I', len(res))
        self.send_result(_bytes+res)

    def handle_request(self, data):
        info_dict = loads(data)
        method = info_dict["method"]
        args = info_dict["args"]
        kw = info_dict["kw"]
        future = self._server.dispatch(method, args, kw)
        future.add_done_callback(self._done_callback)
        self.read_message_bytes()

    def send_result(self, data):    
        self._stream.write(data)
            
    def set_on_close(self, f):
        if callable(f):
            self._stream.set_close_callback(f)


class RPCTCPServer(TCPServer):
    def handle_stream(self, stream, address):
        Connection(self, stream, address)

    @gen.coroutine
    def dispatch(self, method_name, args, kw):
        method = getattr(self, method_name, None)
        if not callable(method) or getattr(method, 'private', False):
            raise gen.Return({'status': METHOD_NOT_FOUND})
        try:
            response = method(*args, **kw)
        except Exception:
            raise gen.Return({'status': INTERNAL_ERROR})
        
        if is_future(response) :
            response = yield response
        
        raise gen.Return({'status': SUCCESS, 'result': response})