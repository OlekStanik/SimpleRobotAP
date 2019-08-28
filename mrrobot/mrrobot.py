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
from .conversation import conversation_json

def jump(link, root):
    for k in link:
        root = root[k]
    return root


class MrRobot(object):
    ''' MrRobot is single instance chatbot interface.
        Every droid session has unique uuid (droidId)
        To start discussion please use 'hello' command
        by sending string query to 'get_response' member
    '''    
    def __init__(self, droidId, name = "Elliot"):
        self.__name = name
        self.__droidId = str(uuid.UUID(droidId))
        self.__memory = conversation_json
        self.__root = self.__memory
        self.__EoC = False
        self.__result = -1

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self,value):
        if (type(value) is str):
            self.__name = value

    @property
    def droidId(self):
        return self.__droidId

    def get_response(self, query):
        if self.__EoC: return

        query = str(query == self.__result) if query.isdigit() else query
        query = query.lower()

        if query in self.__memory:
            self.__memory = self.__memory[query]
            if "link" in self.__memory.keys():
                self.__memory = jump(self.__memory["link"],self.__root)
            if "response" in self.__memory.keys():
                text = self.__memory["response"]
                if "action" in self.__memory.keys():
                    if self.__memory["action"]:
                        text, self.__result = self.__memory["action"](text)
                if "EoC" in text: self.__EoC = True
                return text
        return "Sorry I don't understand. Could you repeat please?"

    