import unittest
from tornado import gen
from tornado.websocket import WebSocketClientConnection
from tornado.ioloop import IOLoop
from gremlinclient import GremlinFactory
from gremlinclient import GremlinPool


class TornadoPEP492SyntaxTest(unittest.TestCase):

    def setUp(self):
        self.loop = IOLoop.current()
        self.factory = GremlinFactory()
        self.pool = GremlinPool(factory=self.factory, maxsize=2)

    def test_connect(self):

        async def go():
            connection = self.factory.connect()
            conn = await connection.conn
            self.assertIsNotNone(conn.protocol)
            self.assertIsInstance(conn, WebSocketClientConnection)
            conn.close()

        self.loop.run_sync(go)

    def test_submit(self):

        async def go():
            connection = self.factory.connect()
            resp = await connection.submit("1 + 1")
            while True:
                msg = await resp.read()
                if msg is None:
                    break
                self.assertEqual(msg.status_code, 200)
                self.assertEqual(msg.data[0], 2)

        self.loop.run_sync(go)

if __name__ == "__main__":
    unittest.main()
