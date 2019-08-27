#-----------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
#-----------------------------------------------------------------------------------------
import uuid

class MrRobot(object):
    def __init__(self, droidId):
        
        self.__name = "Elliot"
        self.__droidId = str(uuid.UUID(droidId))

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
    