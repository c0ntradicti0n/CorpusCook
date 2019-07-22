#!/usr/bin/env python

# WS client example

import asyncio
import json
import random

import websocket
import websockets
from more_itertools import consumer

"""
message = '{"command": "make_prediction", "text": "I am good. You are bad."}'

async def handler(message):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        json_message = input() # text_store.next_one()


        #json_message = json.loads(message)
        #if json_message['command'] in client_tasks:
        #    answer = client_tasks[json_message['command']](json_message)


        await websocket.send(str(json_message))
        print(f"> {json_message}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(handler())
"""

from websockets import connect

class EchoWebsocket:
    def __init__(self, uri):
        self.uri = uri

    async def __aenter__(self):
        self._conn = connect(self.uri)
        self.websocket = await self._conn.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    async def send(self, message):
        await self.websocket.send(message)

    async def receive(self):
        return await self.websocket.recv()

class Client:
    def __init__(self, uri):
        self.uri=uri
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main())

    @asyncio.coroutine
    async def main(self):
        async with EchoWebsocket(self.uri) as echo:
            while True:
                await echo.send(str(await (yield)))
                print(await echo.receive())  # "Hello!"





cl = Client(uri="ws://localhost:8765")
x = cl.main()
x.send(None)
x.send('hallo')


