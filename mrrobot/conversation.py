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

from random import randrange

def process_sum(text, num1, num2):
    result = num1 + num2
    return text.format(num1, num2), str(result)

def rand_sum(text):
    return process_sum(text, randrange(10), randrange(10))

def const_sum(text):
    return process_sum(text, 8, 9)
    
conversation_json = { 
    "hello": {  "response": "Are you a droid?",
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
