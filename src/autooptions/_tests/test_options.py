import os

from autooptions.options import Options


class TestOptions:


    def testConstructor(self):
        options = Options("Autooptions Test", "Magic Filter")
        assert options.applicationName == "Autooptions Test"
        assert options.optionsName == "Magic Filter"
        assert os.path.exists(os.path.dirname(options.optionsPath))