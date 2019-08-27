import sys
import os
import unittest
import json
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from mrrobot.mrrobot import MrRobot

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

    def test_droidMessage(self):
        Elliot = MrRobot(str(uuid.uuid4()))
        Elliot.query
if __name__ == '__main__':
    suite = unittest.TestSuite()
    testloader = unittest.TestLoader()
    testnames = testloader.getTestCaseNames(MrRobot_TestCase)
    for test_name in testnames:
        suite.addTest(MrRobot_TestCase(test_name))
    unittest.TextTestRunner(verbosity=2).run(suite)