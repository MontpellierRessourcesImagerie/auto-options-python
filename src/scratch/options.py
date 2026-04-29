import napari
from autooptions.options import Options
from autooptions.widget import OptionsWidget

class Client:


    def __init__(self):
        self.viewer = napari.Viewer()
        self.options = None
        self.widget = None


    def onApplyButtonClicked(self):
        print(self.options.items)


    def onInputChanged(self, value):
        if not value.isnumeric():
            self.widget.widgets["size xy"].setText(str(self.options.value("size xy")))


    def showOptions(self):
        # Create a Qt widget, which will be our window.
        self.options = Options("Test_Auto_Options", "Median Filter")
        self.options.addImage('image', value=None, transient=True)
        self.options.addInt('size xy', value=3, widget="input", callback=self.onInputChanged)
        self.options.addInt('size z', value=1, widget="input")
        self.options.addChoice('footprint', value=None, choices=["none", "cube", "ball", "octahedron"])
        self.options.addInt('radius', value=1, widget="input")
        self.options.load()
        self.widget = OptionsWidget(self.viewer, self.options, self, sameRowMap={"size z": True})
        self.widget.addApplyButton(self.onApplyButtonClicked)
        #self.widget.addOKButton(None)
        #self.widget.addCancelButton(None)
        self.viewer.window.add_dock_widget(self.widget, name=self.options.optionsName)
        self.viewer.show()
        napari.run()

client = Client()
client.showOptions()
