ToRPC
==========

Simple JSON RPC using the Tornado framework.


Usage
=====

Server Usage:

```python
# -*- coding: utf-8 -*-

from torpc.server import RPCTCPServer, private
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from tornado.ioloop import IOLoop

class RPCServerHandler(RPCTCPServer):

    # Can't be called externally
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


if __name__ == "__main__":
    server = RPCServerHandler()    
    server.listen(8890)   
    IOLoop.instance().start()
```

Client Usage:

```python
# -*- coding: utf-8 -*-

from torpc.client import RPCClient
from tornado import gen
from tornado.ioloop import IOLoop 

@gen.coroutine
def test():
    RPC_client = RPCClient()
    yield RPC_client.connect('127.0.0.1', 8890)
    res = yield RPC_client.add(22, 33)
    assert res == 55
    res = yield RPC_client.fetch('http://bing.com')
    assert res == 200

ioloop = IOLoop.current()
ioloop.run_sync(test)
```


Contributing
============

Fork, patch, test, and send a pull request.


License
=======

[MIT](http://opensource.org/licenses/MIT) ©