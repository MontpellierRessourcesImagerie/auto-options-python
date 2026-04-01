import os
import pytest
from autooptions.options import Options


class TestOptions:


    @pytest.fixture()
    def options(self):
        options = Options("Autooptions Test", "Magic Filter")
        options.addImage('image', value=None, transient=True)
        options.addInt('size xy', value=3, widget="input")
        options.addInt('size z', value=1, widget="input")
        options.addChoice('footprint', value=None, choices=["none", "cube", "ball", "octahedron"])
        options.addInt('radius', value=1, widget="input")
        yield options


    def onSomething(self, value):
        pass


    def testConstructor(self):
        options = Options("Autooptions Test", "Magic Filter")
        assert options.applicationName == "Autooptions Test"
        assert options.optionsName == "Magic Filter"
        assert os.path.exists(os.path.dirname(options.optionsPath))


    def testSetDefaultItems(self):
        options = Options("Autooptions Test", "Magic Filter")
        items = {'image': {'value': None, 'type': 'image', 'transient': True, 'position': 0, 'callback': None},
            'size xy': {'type': 'int', 'value': 3, 'transient': False, 'position': 1, 'widget': 'input',
                     'callback': 'onInputChanged'},
         'size z': {'type': 'int', 'value': 1, 'transient': False, 'position': 2, 'widget': 'input', 'callback': None},
         'footprint': {'name': 'footprint', 'value': None, 'type': 'choice',
                       'choices': ['none', 'cube', 'ball', 'octahedron'], 'transient': False, 'position': None,
                       'callback': None},
         'radius': {'type': 'int', 'value': 1, 'transient': False, 'position': 4, 'widget': 'input', 'callback': None}}
        options.setDefaultValues(items)
        assert options.getItems() == items


    def testGetItems(self, options):
        items = options.getItems()
        assert items['size xy']['value'] == 3
        assert list(items.keys()) == ['image', 'size xy', 'size z', 'footprint', 'radius']


    def testSaveAndLoad(self, options):
        if os.path.exists(options.optionsPath):
            os.remove(options.optionsPath)
        oldItems = options.getItems().copy()
        options.load()
        self.items = None
        options.load()
        assert oldItems == options.getItems()


    def testGet(self, options):
        option = options.get("size xy")
        assert option["value"] == 3


    def testValue(self, options):
        value = options.value("size xy")
        assert value == 3


    def testSet(self, options):
        option = {'type': 'int', 'value': 1.365, 'transient': False, 'position': 5, 'widget': 'input', 'callback': None}
        options.set("sigma", option)
        optionRetrieved = options.get("sigma")
        assert optionRetrieved == option



    def testSetValue(self, options):
        options.setValue("size xy", 8)
        assert options.value("size xy") == 8


    def testAddImage(self):
        options = Options("Autooptions Test", "Magic Filter")
        options.addImage('input image', value="img01", transient=True)
        assert options.value("input image") == "img01"
        options.addImage('mask', value="mask", transient=True)
        assert options.value("mask") == "mask"
        assert options.get("mask")["position"] == 2
        assert options.get("mask")["type"] == "image"


    def testAddLabels(self):
        options = Options("Autooptions Test", "Magic Filter")
        options.addLabels('labels', value="img01_seg", transient=True)
        assert options.value("labels") == "img01_seg"
        assert options.get("labels")["type"] == "labels"


    def testAddPoints(self):
        options = Options("Autooptions Test", "Magic Filter")
        options.addPoints('centroids', value="centroids_layer", transient=True)
        assert options.value("centroids") == "centroids_layer"
        assert options.get("centroids")["type"] == "points"


    def testAddFFT(self):
        options = Options("Autooptions Test", "Magic Filter")
        options.addFFT('fft1', value="img01_fft", transient=True)
        assert options.value("fft1") == "img01_fft"
        assert options.get("fft1")["type"] == "fft"


    def testAddInt(self, options):
        options.addInt('threshold', value=50, callback=self.onSomething)
        assert options.get("threshold")["callback"] == "onSomething"
        assert options.value("threshold") == 50
        assert options.get("threshold")["type"] == "int"
        assert options.get("threshold")["widget"] == "input"


    def testAddFloat(self, options):
        options.addFloat('sigma', value=1.3)
        assert options.value("sigma") == 1.3
        assert options.get("sigma")["type"] == "float"
        assert options.get("sigma")["widget"] == "input"


    def testAddChoice(self, options):
        options.addChoice("no choice")
        assert options.value("no choice") is None
        assert options.get("no choice")["type"] == "choice"
        assert options.get("no choice")["choices"] == []
        options.addChoice("fruits", value="apple", choices=["orange", "banana", "apple"])
        assert options.value("fruits") == "apple"
        assert options.get("fruits")["type"] == "choice"
        assert options.get("fruits")["choices"] == ["orange", "banana", "apple"]


    def testAddStr(self, options):
        options.addStr('experimenter', value="Albert")
        assert options.value("experimenter") == "Albert"
        assert options.get("experimenter")["type"] == "str"
        assert options.get("experimenter")["widget"] == "input"


    def testAddBool(self, options):
        options.addBool('use gpu', value=True)
        assert options.value("use gpu") == True
        assert options.get("use gpu")["type"] == "bool"
        assert options.get("use gpu")["widget"] == "checkbox"
        options.addBool('remove background', value=False)
        assert options.value("remove background") == False
        assert options.get("remove background")["type"] == "bool"
        assert options.get("remove background")["widget"] == "checkbox"


    def testGetBaseOption(self, options):
        option = options.getBaseOption(7, True, None, self.onSomething)
        assert option["value"] == 7
        assert option["transient"] == True
        assert option["position"] == 6
        assert option["callback"] == "onSomething"


    def test_GetPosition(self, options):
        position = options._getPosition(None)
        assert position == 6
        position = options._getPosition(3)
        assert position == 3

