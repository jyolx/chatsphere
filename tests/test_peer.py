# tests/test_peer.py
import unittest
from chatsphere import Peer
import asyncio

class TestPeer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create two peers for testing
        cls.peer1 = Peer(port=5000, log_file="test_peer1.log")
        cls.peer2 = Peer(port=5001, log_file="test_peer2.log")

    @classmethod
    def tearDownClass(cls):
        cls.peer1.stop()
        cls.peer2.stop()

    def test_start_peer(self):
        """Test if the peer starts successfully."""
        asyncio.run(self.peer1.start())
        asyncio.run(self.peer2.start(('127.0.0.1', 5000)))
        self.assertIsNotNone(self.peer1.server)
        self.assertIsNotNone(self.peer2.server)

    def test_store_and_retrieve(self):
        """Test if the store and retrieve functionality works."""
        asyncio.run(self.peer1.start())
        asyncio.run(self.peer2.start(('127.0.0.1', 5000)))

        key, value = "testKey", "testValue"
        asyncio.run(self.peer1.store(key, value))
        retrieved_value = asyncio.run(self.peer2.retrieve(key))

        self.assertEqual(retrieved_value, value)

if __name__ == '__main__':
    unittest.main()
