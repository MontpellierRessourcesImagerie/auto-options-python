import sys
from qtpy.QtWidgets import QApplication
from autooptions.options import Options
from autooptions.widget import OptionsWidget


app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
options = Options("Test_Auto_Options", "Median Filter")
options.addImage(name='image', value=None, transient=True)
options.addInt(name='size xy', value=3, widget="input")
options.addInt(name='size z', value=1, widget="input")
options.addChoice(name='footprint', value=None, choices=["none", "cube", "ball", "octahedron"])
options.addInt(name='radius', value=1, widget="input")
window = OptionsWidget(None, options)
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()