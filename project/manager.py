import uvicorn
import asyncio
from project.backend.server import back_app
from project.client.server_client import client_root


class ManagerServer:
    def __init__(self):
        self.m = 12

    @staticmethod
    async def app():
        config_a = uvicorn.Config(back_app, host="127.0.0.1", port=8000, log_level="debug")
        server_a = uvicorn.Server(config_a)

        config_b = uvicorn.Config(client_root, host="127.0.0.1", port=8001, log_level="debug")
        server_b = uvicorn.Server(config_b)

        await asyncio.gather(
            server_a.serve(),
            server_b.serve(),

        )
