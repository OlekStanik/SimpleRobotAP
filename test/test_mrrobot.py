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

import sys
import os
import unittest
import json
import uuid
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from mrrobot.mrrobot import MrRobot

def extractAndSum(input):
    results =  re.findall('\d+', input)
    return sum([int(i) for i in results])

myjson = {"one":{"two":{"three":101}}}

class MrRobot_TestCase(unittest.TestCase):
    def test_init(self):
        Elliot = MrRobot(str(uuid.uuid4()))
        self.assertEqual(Elliot.name,"Elliot")

    def test_name(self):
        Elliot = MrRobot(str(uuid.uuid4()))
        Elliot.name = "Ollie"
        self.assertEqual(Elliot.name,"Ollie")
        Elliot.name = 123
        self.assertEqual(Elliot.name,"Ollie")
        Elliot.name = bytearray("MrRobot", 'utf-8')
        self.assertEqual(Elliot.name,"Ollie")
        Elliot.name = "Elliot"
        self.assertEqual(Elliot.name,"Elliot")

    def test_droidId(self):
        droidId = str(uuid.uuid4())
        print (droidId)
        Elliot = MrRobot(droidId)
        self.assertEqual(Elliot.droidId,droidId)
        Ollie = None
        try:
            Ollie = MrRobot("1234")
        except ValueError:
            pass
        finally:
            self.assertNotIsInstance(Ollie, MrRobot)

    def test_droidMessagePositiveScenario1(self):
        Elliot = MrRobot(str(uuid.uuid4()))
        self.assertEqual(Elliot.get_response("HELLO"),"Are you droid?")
        self.assertEqual(Elliot.get_response("YES"),"So then, prove you can do some math. What is the sum of 8 and 9?")
        self.assertEqual(Elliot.get_response("17"),"You are right! Wanna try another one?")
        answere = Elliot.get_response("yeS")
        self.assertIn("What is the sum of ",answere)
        value = extractAndSum(answere)
        self.assertEqual(Elliot.get_response(str(value)),"You are right! I’ll remember you can do the maths! EoC")
        self.assertIsNone(Elliot.get_response("33"))

    def test_droidMessageNegativeScenario1(self):
        Elliot = MrRobot(str(uuid.uuid4()))
        self.assertEqual(Elliot.get_response("heLLO"),"Are you droid?")
        self.assertEqual(Elliot.get_response("YEs"),"So then, prove you can do some math. What is the sum of 8 and 9?")
        answere = Elliot.get_response("31")
        self.assertIn("Let's try again. What is the sum of ",answere)
        value = extractAndSum(answere)
        self.assertEqual(Elliot.get_response(str(value)),"You are right! Wanna try another one?")
        answere = Elliot.get_response("yeS")
        self.assertIn("What is the sum of ",answere)
        value = extractAndSum(answere)
        self.assertEqual(Elliot.get_response(str(value)),"You are right! I’ll remember you can do the maths! EoC")
        self.assertIsNone(Elliot.get_response("heLLO34325412451t1r4"))

    def test_droidMessageNegativeScenario2(self):
        Elliot = MrRobot(str(uuid.uuid4()))
        self.assertEqual(Elliot.get_response("heLLO"),"Are you droid?")
        self.assertEqual(Elliot.get_response("nO"),"That's so sad. EoC")
        self.assertIsNone(Elliot.get_response("heLLO"))

    def test_droidMessageNegativeScenario3(self):
        Elliot = MrRobot(str(uuid.uuid4()))
        self.assertEqual(Elliot.get_response("heLLO"),"Are you droid?")
        self.assertEqual(Elliot.get_response("nO"),"That's so sad. EoC")
        self.assertIsNone(Elliot.get_response("heLLO"))
        

if __name__ == '__main__':
    suite = unittest.TestSuite()
    testloader = unittest.TestLoader()
    testnames = testloader.getTestCaseNames(MrRobot_TestCase)
    for test_name in testnames:
        suite.addTest(MrRobot_TestCase(test_name))
    unittest.TextTestRunner(verbosity=2).run(suite)