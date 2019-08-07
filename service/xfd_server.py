#!/usr/bin/python3

import asyncio
import datetime
import requests
import json

import xfd_server_db as db

class XfdServer:

    def __init__(self, path_to_database=""):
        self._database = db.XfdServerDb(path_to_database)
        self._address = self._database.load_address()

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._main(loop))
        loop.close()

    async def _main(self, loop):
        while True:
            print (datetime.datetime.now())
            await self._update() # todo run asynchronous
            await asyncio.sleep(5)

    async def _update(self):
        try:
            print("update")
            response = requests.post(self._address)
            json_obj = json.load(response.text) 

            ## todo update only when the result is newer
            self._database.save_result(json_obj)
        except requests.exceptions.ConnectionError as ex:
            print(ex)


