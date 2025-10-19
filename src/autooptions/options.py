import os
import appdirs
import json
from copy import copy



class Options:


    def __init__(self, applicationName, optionsName):
        self.optionsName = optionsName
        self.applicationName = applicationName
        self.items = {}
        self.defaultItems = None
        self.dataFolder = appdirs.user_data_dir(self.applicationName)
        os.makedirs(self.dataFolder, exist_ok=True)
        self.optionsPath = os.path.join(self.dataFolder, self.optionsName + "_options.json")


    def setDefaultValues(self, defaultItems):
        self.defaultItems = defaultItems


    def getItems(self):
        if not self.items and self.defaultItems:
            self.items = copy(self.defaultItems)
        return self.items


    def save(self):
        with open(self.optionsPath, 'w') as f:
            json.dump(self.getItems(), f)


    def load(self):
        if not os.path.exists(self.optionsPath):
            self.save()
        with open(self.optionsPath) as f:
            self.items = json.load(f)


    def get(self, name):
        return self.items[name]


    def set(self, name, value):
        self.items[name] = value


    def addImage(self, name='image', value=None, transient=True, position=None):
        position = self._getPosition(position)
        self.items[name] = {'value': value,
                            'transient': transient,
                            'position': position}


    def addInt(self, name='size', type=int, value=1, transient=False, position=None, widget="input"):
        position = self._getPosition(position)
        self.items[name] = {'type': type,
                            'value': value,
                            'transient': transient,
                            'position': position,
                            'widget': widget}


    def addChoice(self, name="footprint", value=None, choices=None, transient=False, position=None):
        if not choices:
            choices = []
        self.items[name] = {
            'name': name,
            'value': value,
            'choices': choices,
            'transient': transient,
            'position': position
        }




    def _getPosition(self, position):
        if not position:
            position = len(self.items.keys())
        return position