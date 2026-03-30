import os
import appdirs
import json
from copy import copy



class Options:
    """ Options are a list of parameters that are intended to be passed to an operation. Options have
    a name, a type and a value.
    """


    def __init__(self, applicationName, optionsName):
        """
        Construct an empty Options object for an operation within an application.

        The options will be saved into a file optionsName in the subfolder applicationName of the user-data-folder.
        Spaces in the names will be replaced by underscores in the folder and filename.

        :param applicationName: The name of the application
        :param optionsName: The name of the options
        """
        self.optionsName = optionsName
        self.applicationName = applicationName
        self.items = {}
        self.defaultItems = None
        appName = self.applicationName.replace(' ', '_')
        self.dataFolder = appdirs.user_data_dir(appName)
        os.makedirs(self.dataFolder, exist_ok=True)
        optName = self.optionsName.replace(' ', '_')
        self.optionsPath = os.path.join(self.dataFolder, optName + "_options.json")


    def setDefaultValues(self, defaultItems):
        """
        Set the default values for all options in the options object. Currently unused. The idea is that it might be
        useful to have default values, other than in the code, to which the option can be reset.

        :param defaultItems: A dictionary of default values for all options in the options object.
        """
        self.defaultItems = defaultItems


    def getItems(self):
        """
        Return the items stored in the options object.
        :return: A dictionary of all options in the options object.
        """
        if not self.items and self.defaultItems:
            self.items = copy(self.defaultItems)
        return self.items


    def save(self):
        """
        Save the options as a JSON file.
        """
        with open(self.optionsPath, 'w') as f:
            json.dump(self.getItems(), f)


    def load(self):
        """
        Load the options as a JSON file.
        """
        if not os.path.exists(self.optionsPath):
            self.save()
        with open(self.optionsPath) as f:
            items = json.load(f)
        for key, value in items.items():
            if value['transient']:
                continue
            self.items[key] = value


    def get(self, name):
        """
        Answer the option with the given name.
        :param name: The name of an option
        :return: Answers the option with the given name as a dictionary
        """
        return self.items[name]


    def value(self, name):
        """
        Answer the value of the option with the given name.
        :param name: The name of an option
        :return: The value of the option with the given name. The type of the result depends on the type of the option.
        """
        return self.get(name)['value']


    def set(self, name, value):
        """
        Set the value of the option with the given name.

        :param name: The name of an option
        :param value: The new value of the option
        """
        self.items[name] = value


    def addImage(self, name='image', value=None, transient=True, position=None, callback=None):
        """
        Add an option that represents the selection of an image. Image options are often transient.

        :param name: The name of the image option
        :param value: The value of the image option
        :param transient: Whether the image option is transient. Transient options are not saved and reloaded.
        :param position: The position of the image option within the options (Could be used when dictionaries are not
                         ordered). If none is given, the next free position is used.
        :param callback: The callback function, that is called when the value of the option is changed.
        """
        position = self._getPosition(position)
        self.items[name] = {'value': value,
                            'type': 'image',
                            'transient': transient,
                            'position': position,
                            'callback': callback}


    def addFFT(self, name='image', value=None, transient=True, position=None, callback=None):
        position = self._getPosition(position)
        self.items[name] = {'value': value,
                            'type': 'fft',
                            'transient': transient,
                            'position': position,
                            'callback': callback}


    def addInt(self, name, value=1, transient=False, position=None, widget="input", callback=None):
        position = self._getPosition(position)
        callbackQualifiedName = None
        if callback:
            callbackQualifiedName = callback.__name__
        self.items[name] = {'type': 'int',
                            'value': value,
                            'transient': transient,
                            'position': position,
                            'widget': widget,
                            'callback': callbackQualifiedName}


    def addFloat(self, name, value=0.0, transient=False, position=None, widget="input", callback=None):
        position = self._getPosition(position)
        self.items[name] = {'type': 'float',
                            'value': value,
                            'transient': transient,
                            'position': position,
                            'widget': widget,
                            'callback': callback}


    def addChoice(self, name="footprint", value=None, choices=None, transient=False, position=None, callback=None):
        if not choices:
            choices = []
        self.items[name] = {
            'name': name,
            'value': value,
            'type': 'choice',
            'choices': choices,
            'transient': transient,
            'position': position,
            'callback': callback
        }


    def addStr(self, name, value="", transient=False, position=None, callback=None):
        position = self._getPosition(position)
        self.items[name] = {'type': 'str',
                            'value': value,
                            'transient': transient,
                            'position': position,
                            'widget': "input",
                            'callback': callback}


    def addBool(self, name, value=False, transient=False, position=None, callback=None):
        position = self._getPosition(position)
        self.items[name] = {'type': 'bool',
                            'value': value,
                            'transient': transient,
                            'position': position,
                            'widget': "checkbox",
                            'callback': callback}


    def _getPosition(self, position):
        if not position:
            position = len(self.items.keys())
        return position