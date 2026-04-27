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
        Return a copy of the items stored in the options object.

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
            if value['transient'] or key not in self.items:
                continue
            self.items[key] = value


    def get(self, name, alt=None):
        """
        Answer the option with the given name.

        :param name: The name of an option
        :param alt: The alternative value to return if the option is not found
        :return: Answers the option with the given name as a dictionary or the alternative.
        """
        return self.items.get(name, alt)


    def value(self, name):
        """
        Answer the value of the option with the given name.

        :param name: The name of an option
        :return: The value of the option with the given name. The type of the result depends on the type of the option. If the option is optional and not active, None is returned.
        """
        if self.get(name)['optional'] and not self.get(name)['active']:
            return None
        return self.get(name)['value']
    

    def isActive(self, name):
        """
        Answer whether the option with the given name is active. An option is active if it is not optional or if it is
        optional and has a value that is not None.

        :param name: The name of an option
        :return: True if the option with the given name is active and False otherwise.
        """
        return not self.get(name)['optional'] or self.get(name)['active']


    def set(self, name, option):
        """
        Set the option in options under the given name.

        :param name: The name of an option
        :param option: The new option
        """
        self.items[name] = option


    def setValue(self, name, value):
        """
        Set the value of the option with the given name to value.
        If the option is optional and not active, the value will not be set.

        :param name: The name of an option
        :param value: The new value of the option
        """
        if self.get(name)['optional'] and not self.get(name)['active']:
            return
        self.get(name)['value'] = value


    @classmethod
    def getCallbackName(cls, callback):
        callbackName = None
        if callback:
            callbackName = callback.__name__
        return callbackName


    def addImage(self, name='image', value=None, transient=True, position=None, callback=None, optional=False):
        """
        Add an option that represents the selection of an image. Image options are often transient.

        :param name: The name of the image option
        :param value: The value of the image option
        :param transient: Whether the image option is transient. Transient options are not saved and reloaded.
        :param position: The position of the image option within the options (Could be used when dictionaries are not
                         ordered). If none is given, the next free position is used.
        :param callback: The callback function, that is called when the value of the option is changed.
        :optional: Whether the image is optional and whether it should start active or not.
        """
        self.set(name, self._getBaseOption(value, transient, position, callback, optional) | {
                            'type': 'image'})


    def addLabels(self, name='labels', value=None, transient=True, position=None, callback=None, optional=False):
        """
        Add an option that represents the selection of a labels image. Labels options are often transient.

        :param name: The name of the labels option
        :param value: The value of the labels option
        :param transient: Whether the labels option is transient. Transient options are not saved and reloaded.
        :param position: The position of the labels option within the options (Could be used when dictionaries are not
                         ordered). If none is given, the next free position is used.
        :param callback: The callback function, that is called when the value of the option is changed.
        :param optional: Whether the labels option is optional and whether it should start active or not.
        """
        self.set(name, self._getBaseOption(value, transient, position, callback, optional) | {
            'type': 'labels'})


    def addFFT(self, name='fft', value=None, transient=True, position=None, callback=None, optional=False):
        """
        Add an option that represents the selection of an FFT image. Image options are often transient. The FFT
        is not a standard image, since only the amplitude information is in the image, while the phase information is
        kept in the metadata.

        :param name: The name of the option
        :param value: The name of the fft layer
        :param transient: Whether the fft option is transient. Transient options are not saved and reloaded.
        :param position: The position of the fft option within the options. (Could be used when dictionaries are not
                         ordered). If none is given, the next free position is used.
        :param callback: A callback function, that is called when the selected fft layer changes
        :param optional: Whether the fft option is optional and whether it should start active or not.
        """
        self.set(name, self._getBaseOption(value, transient, position, callback, optional) | {
                            'type': 'fft'})


    def addPoints(self, name='points', value=None, transient=True, position=None, callback=None, optional=False):
        """
        Add an option that represents the selection of a points layer. Points options are often transient.

        :param name: The name of the points option
        :param value: The value of the points option
        :param transient: Whether the points option is transient. Transient options are not saved and reloaded.
        :param position: The position of the points option within the options (Could be used when dictionaries are not
                         ordered). If none is given, the next free position is used.
        :param callback: The callback function, that is called when the value of the option is changed.
        :param optional: Whether the points option is optional and whether it should start active or not.
        """
        self.set(name, self._getBaseOption(value, transient, position, callback, optional) | {
            'type': 'points'})


    def addInt(self, name, value=1, transient=False, position=None, widget="input", callback=None, optional=False):
        """
        An option that represents an integer value.

        :param name: The name of the option
        :param value: The integer value
        :param transient: Whether the option is transient. Transient options are not saved and reloaded.
        :param position: The position of the option within the options. (Could be used when dictionaries are not
                         ordered). If none is given, the next free position is used.
        :param widget: Currently only the input-widget, which means entering the number into an input field, is
                       implemented. However, an integer could also be entered in a different way, for example using
                       a slider.
        :param callback: A callback function, that is called when the value is changed via the graphical interface.
        :param optional: Whether the integer is optional and whether it should start active or not.
        """
        self.set(name, self._getBaseOption(value, transient, position, callback, optional) | {
                            'type': 'int',
                            'widget': widget})


    def addFloat(self, name, value=0.0, transient=False, position=None, widget="input", callback=None, optional=False):
        """
        An option that represents a float value.

        :param name:  The name of the option
        :param value: The float value
        :param transient: Whether the option is transient. Transient options are not saved and reloaded.
        :param position: The position of the option within the options. (Could be used when dictionaries are not
                         ordered). If none is given, the next free position is used.
        :param widget: Currently only the input-widget, which means entering the number into an input field, is
                       implemented. However, a float could also be entered in a different way, for example using
                       a slider.
        :param callback: A callback function, that is called when the value is changed via the graphical interface.
        :param optional: Whether the float is optional and whether it should start active or not.
        """
        self.set(name, self._getBaseOption(value, transient, position, callback, optional) | {
                            'type': 'float',
                            'widget': widget})


    def addChoice(self, name, value=None, choices=None, transient=False, position=None, callback=None, optional=False):
        """
        An option that represents a choice in a list of given values.

        :param name: The name of the option
        :param value: The text of the selected choice
        :param choices: A collection of possible values
        :param transient: Whether the option is transient. Transient options are not saved and reloaded.
        :param position: The position of the option within the options. (Could be used when dictionaries are not
                         ordered). If none is given, the next free position is used.
        :param callback: A callback function, that is called whenever the selected item is changed, whether via the gui
                         or programmatically. The implementer must take care to avoid endless loops.
        :param optional: Whether the choice is optional and whether it should start active or not.
        """
        if not choices:
            choices = []
        self.set(name, self._getBaseOption(value, transient, position, callback, optional) | {
            'type': 'choice',
            'choices': choices})


    def addStr(self, name, value="", transient=False, position=None, callback=None, optional=False):
        """
        An option that represents a textual value.

        :param name:  The name of the option
        :param value: The text
        :param transient: Whether the option is transient. Transient options are not saved and reloaded.
        :param position: The position of the option within the options. (Could be used when dictionaries are not
                         ordered). If none is given, the next free position is used.
        :param callback: A callback function, that is called when the value is changed via the graphical interface.
        :param optional: Whether the string is optional and whether it should start active or not.
        """
        self.set(name,
                 self._getBaseOption(value, transient, position, callback, optional) | {
                     'type': 'str',
                     'widget': "input"})


    def addBool(self, name, value=False, transient=False, position=None, callback=None, optional=False):
        """
        An option that represents a binary choice.

        :param name: The name of the option
        :param value: The boolean value, True or False
        :param transient: Whether the option is transient. Transient options are not saved and reloaded.
        :param position: The position of the option within the options. (Could be used when dictionaries are not
                         ordered). If none is given, the next free position is used.
        :param callback: A callback function, that is called whenever the selected item is changed, whether via the gui
                         or programmatically. The implementer must take care to avoid endless loops.
        :param optional: Whether the boolean is optional and whether it should start active or not.
        """
        self.set(name,
                 self._getBaseOption(value, transient, position, callback, optional) | {
                     'type': 'bool',
                     'widget': "checkbox"})
    

    def addFolder(self, name='folder', value="", transient=True, position=None, callback=None, optional=False):
        """
        Add an option that represents the selection of a folder. Folder options are often transient.

        :param name: The name of the folder option
        :param value: The value of the folder option (path)
        :param transient: Whether the folder option is transient. Transient options are not saved and reloaded.
        :param position: The position of the folder option within the options (Could be used when dictionaries are not
                         ordered). If none is given, the next free position is used.
        :param callback: The callback function, that is called when the value of the option is changed.
        :param optional: Whether the folder option is optional and whether it should start active or not.
        """
        self.set(name, self._getBaseOption(value, transient, position, callback, optional) | {
            'type': 'folder'})
        

    def addFile(self, name='file', value="", transient=True, position=None, callback=None, optional=False):
        """
        Add an option that represents the selection of a file. File options are often transient.

        :param name: The name of the file option
        :param value: The value of the file option (path)
        :param transient: Whether the file option is transient. Transient options are not saved and reloaded.
        :param position: The position of the file option within the options (Could be used when dictionaries are not
                         ordered). If none is given, the next free position is used.
        :param callback: The callback function, that is called when the value of the option is changed.
        :param optional: Whether the file option is optional and whether it should start active or not.
        """
        self.set(name, self._getBaseOption(value, transient, position, callback, optional) | {
            'type': 'file'})
    

    def _getBaseOption(self, value, transient, position, callback, optional):
        """
        A helper method to set the parts of an option that a common to all kinds of options.

        :param value:  The value of the option
        :param transient: Whether the option is transient. Transient options are not saved and reloaded.
        :param position: The position of the option within the options. (Could be used when dictionaries are not
                         ordered). If none is given, the next free position is used.
        :param callback: A callback function, that is called when the value of the option changes.
        """
        if type(optional) == bool:
            optional = optional
            active = True
        elif type(optional) == tuple and len(optional) == 2:
            optional, active = optional
        else:
            raise ValueError("optional must be either a boolean or a tuple of two booleans")
        
        return { 
            'value'    : value,
            'transient': transient,
            'position' : self._getPosition(position),
            'callback' : self.getCallbackName(callback),
            'optional' : optional,
            'active'   : active
        }


    def _getPosition(self, position):
        """
        If the position is None, the next free position is returned. The next free position is the
        maximal position plus one. If position is not None, the given position is returned.

        :param position: None or a non-negative integer
        :return: A non-negative integer, which is either the given position or the next free position
        """
        if not position:
            positions = [option["position"] for option in self.items.values()]
            if positions:
                position = max([option["position"] for option in self.items.values()]) + 1
            else:
                position = 1
        return position