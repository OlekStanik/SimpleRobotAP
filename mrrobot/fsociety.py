# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Written by Olek Stanik <olek.stanik@gmail.com>, August 2019

import uuid
import json
import sqlite3
from datetime import datetime

from .mrrobot import MrRobot

def pack_json_msg(msg, droidId):
    return {"message":msg, "droidId": str(droidId)}

class FSociety(object):
    ''' FSociety is main interface responsible for
        multisession chatbot communication based on
        json requests with build in archiver.
    '''
    def __init__(self):
        self.__MrRobotDict = dict()
        self.__db = sqlite3.connect('archive.db')
        cur = self.__db.cursor()
        cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='story' ''')
        #if the count is 1, then table exists
        if cur.fetchone()[0]!=1 : {
	        cur.execute("CREATE TABLE story('droidId' text , 'date' DATE, 'typ' text, 'msg' text)")
        }
        self.__db.commit()

    def archive(self, req, res, droidId):
        cur = self.__db.cursor()
        cur.execute('''INSERT INTO story VALUES (?,?,?,?)''' , [droidId, datetime.now(), "Q", req])
        cur.execute('''INSERT INTO story VALUES (?,?,?,?)''' , [droidId, datetime.now(), "A", res])
        self.__db.commit()
    
    def query(self, query):
        mrRobot = None
        if query["message"] is "hello":
            mrRobot = MrRobot(query["droidId"])
            self.__MrRobotDict[mrRobot.droidId] = mrRobot

        if query["droidId"] in self.__MrRobotDict.keys():
            mrRobot = self.__MrRobotDict[query["droidId"]]
            request = query["message"]
            response = mrRobot.get_response(request)
            self.archive(request, response, mrRobot.droidId)
            return pack_json_msg(response,mrRobot.droidId)
        return pack_json_msg("", query["droidId"])

    def kill(self, droidId):
        self.__MrRobotDict.pop(droidId, None)

    def get_history(self, droidId, vdate):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM story WHERE droidId=? AND date >?" , [droidId,vdate])
        self.__db.commit()
        rows = cur.fetchall()
        return rows