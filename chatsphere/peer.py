from kademlia.network import Server
import asyncio
import logging

class Peer:
    def __init__(self, port, log_file="peer.log"):
        self.server = Server()
        self.port = port
        self.logger = logging.getLogger(f"Peer-{port}")
        self._setup_logger(log_file)

    def _setup_logger(self, log_file):
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def start(self, bootstrap_node=None):
        await self.server.listen(self.port)
        if bootstrap_node:
            await self.server.bootstrap([bootstrap_node])
            self.logger.info(f"Bootstrapped to node {bootstrap_node}")

    async def store(self, key, value):
        await self.server.set(key, value)
        self.logger.info(f"Stored key: {key} with value: {value}")

    async def retrieve(self, key):
        value = await self.server.get(key)
        self.logger.info(f"Retrieved key: {key} with value: {value}")
        return value

    def stop(self):
        self.server.stop()
        self.logger.info("Server stopped")
