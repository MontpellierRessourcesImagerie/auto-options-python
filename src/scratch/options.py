import napari
from autooptions.options import Options
from autooptions.widget import OptionsWidget

class Client:

    def __init__(self):
        self.viewer = napari.Viewer()
        self.options = None
        self.widget = None


    def onInputChanged(self, value):
        if not value.isnumeric():
            self.widget.widgets["size xy"].setText(str(self.options.value("size xy")))


    def showOptions(self):
        # Create a Qt widget, which will be our window.
        self.options = Options("Test_Auto_Options", "Median Filter")
        self.options.addImage(name='image', value=None, transient=True)
        self.options.addInt(name='size xy', value=3, widget="input", callback=self.onInputChanged)
        self.options.addInt(name='size z', value=1, widget="input")
        self.options.addChoice(name='footprint', value=None, choices=["none", "cube", "ball", "octahedron"])
        self.options.addInt(name='radius', value=1, widget="input")
        self.options.load()
        self.widget = OptionsWidget(self.viewer, self.options, self)
        self.viewer.window.add_dock_widget(self.widget)
        self.viewer.show()
        napari.run()

client = Client()
client.showOptions()