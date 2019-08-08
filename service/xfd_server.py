#!/usr/bin/python3

import asyncio
import datetime
import requests
import json

import xfd_server_db as db

class XfdServer:

    def __init__(self, path_to_database=""):
        self._database = db.XfdServerDb(path_to_database)
        (self._job_id, self._address) = self._database.load_address()

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
            # print("update")
            response = requests.post(self._address + "/lastBuild/api/json?pretty=true&tree=number,result,url")

            print (response)

            json_obj = json.loads(response.text) 

            # json_obj = {
            #     "number" : "1",
            #     "result" : "SUCCESS",
            #     "url" : "http://hogehoge.jp",
            # }

            build_id = json_obj["number"]
            build_result = json_obj["result"]
 
            ## todo update only when the result is newer
            exists, latest_build_id, state_id = self._database.get_latest_result(self._job_id)

            # print (build_id, ", ", latest_build_id, ", ", state_id)

            newdata = (not exists) or (build_id != latest_build_id)

            if newdata:
                print ("New Result [{}] : {}".format(build_id,state_id))

                # TODO control xfd device
                
                self._database.save_result(self._job_id, build_id, build_result)
            else:
                print ("Existing Result [{}] : {}".format(build_id,state_id))

        except requests.exceptions.ConnectionError as ex:
            print(ex)


