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
from random import randrange

def process_sum(text, num1, num2):
    result = num1 + num2
    return text.format(num1, num2), str(result)

def rand_sum(text):
    return process_sum(text, randrange(10), randrange(10))

def const_sum(text):
    return process_sum(text, 8, 9)

def jump(link, root):
    for k in link:
        root = root[k]
    return root

conversation_json = { 
    "hello": {  "response": "Are you droid?",
        "yes": {    "response": "So then, prove you can do some math. What is the sum of {0} and {1}?", "action": const_sum,
            "true": {   "response": "You are right! Wanna try another one?",
                "yes": { "response" :"What is the sum of {0} and {1}?", "action": rand_sum,
                    "true": { "response": "You are right! I’ll remember you can do the maths! EoC"},
                    "false":{"response": "Nice try, human! EoC"}},
                "no": {"response": "I see... Nice try, human! EoC"}},
            "false": { "response": "Let's try again. What is the sum of {0} and {1}?", "action": const_sum,
                "true": {"link":["hello", "yes", "true"]},
                "false": {"link":["hello", "yes", "false"]}}},
        "no": { "response": "That's so sad. EoC"}}
}


class MrRobot(object):
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

    