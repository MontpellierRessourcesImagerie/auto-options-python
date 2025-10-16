from autooptions.options import Options
from qtpy.QtWidgets import QWidget



class OptionsWidget(QWidget):


    def __init__(self, viewer, app, name):
        super().__init__()
        self.viewer = viewer
        self.application = app
        self.name = name
        self.options = Options(self.application, self.name)
        self.fieldWidth = 50


    def _onOKButtonClicked(self):
        self.transferValues()
        self.options.save()
        self.options.load()
        self.shut()


    def _onCancelButtonClicked(self):
        self.shut()


    def shut(self):
        self.viewer.window.remove_dock_widget(self)
        self.close()


    def transferValues(self):
        self.subclassResponsability()


    def ignoreChange(self):
        pass

