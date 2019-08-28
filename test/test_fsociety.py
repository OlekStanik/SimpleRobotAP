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
from  datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from mrrobot.fsociety import FSociety, pack_json_msg

print(str(date.today()))

class FSociety_TestCase(unittest.TestCase):

    fsociety = FSociety()
    droidId = None
    def checkQueryToFSociety(self,fsociety, query, answere, droidId):
        json_query = pack_json_msg(query,droidId)
        json_answere = fsociety.query(json_query)
        json_expected_answere = pack_json_msg(answere,droidId)
        self.assertEqual(json_answere, json_expected_answere)
        print (json_query)
        print (json_answere)

    def test_init(self):
        fsociety = self.fsociety
        self.assertIsInstance(fsociety,FSociety)

    def test_start(self):
        fsociety = self.fsociety
        droidId1 = str(uuid.uuid4())
        self.droidId = droidId1

        self.checkQueryToFSociety(fsociety,"hello","Are you a droid?",droidId1)
        self.checkQueryToFSociety(fsociety,"yEs","So then, prove you can do some math. What is the sum of 8 and 9?",droidId1)

        droidId2 = str(uuid.uuid4())
        self.checkQueryToFSociety(fsociety,"hello","Are you a droid?",droidId2)
        self.checkQueryToFSociety(fsociety,"17","You are right! Wanna try another one?",droidId1)

        self.checkQueryToFSociety(fsociety,"#Dfwerw323rr32145t1rfB!!@#$!","Sorry I don't understand. Could you repeat please?",droidId2)
        self.checkQueryToFSociety(fsociety,"No","I see... Nice try, human! EoC",droidId1)

        self.checkQueryToFSociety(fsociety,"YES","So then, prove you can do some math. What is the sum of 8 and 9?",droidId2)
        self.checkQueryToFSociety(fsociety,"YES",None,droidId1)

        self.test_history()
        
    def test_history(self):
        fsociety = self.fsociety
        current_date = date.today()
        fsociety.get_history(self.droidId,current_date)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    testloader = unittest.TestLoader()
    testnames = testloader.getTestCaseNames(FSociety_TestCase)
    for test_name in testnames:
        suite.addTest(FSociety_TestCase(test_name))
    unittest.TextTestRunner(verbosity=2).run(suite)