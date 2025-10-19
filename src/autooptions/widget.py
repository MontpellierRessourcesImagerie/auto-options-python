from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

from autooptions.options import Options
from qtpy.QtWidgets import QWidget
from autooptions.qtutil import WidgetTool
from autooptions.napari_util import NapariUtil

class OptionsWidget(QWidget):


    def __init__(self, viewer, options):
        super().__init__()
        self.setWindowTitle(options.optionsName)
        self.viewer = viewer
        self.options = options
        self.fieldWidth = 50
        self.imageLayers = []
        self.napariUtil = NapariUtil(viewer)
        self.createLayout()


    def createLayout(self):
        mainLayout = QVBoxLayout()
        for name, item in self.options.items.items():
            if item['type'] == 'image':
                layout = self.getImageWidget(name, item)
                mainLayout.addLayout(layout)
            if item['type'] == 'int':
                layout = self.getIntWidget(name, item)
                mainLayout.addLayout(layout)
            if item['type'] == 'choice':
                layout = self.getChoiceWidget(name, item)
                mainLayout.addLayout(layout)
        self.setLayout(mainLayout)


    def getImageWidget(self, name, item):
        layout = QHBoxLayout()
        self.imageLayers = self.napariUtil.getImageLayers()
        label, widget = WidgetTool.getComboInput(self,
                                                 name+":",
                                                 self.imageLayers)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout


    def getIntWidget(self, name, item):
        layout = QHBoxLayout()
        label, widget = WidgetTool.getLineInput(self,
                                                name,
                                                item['value'],
                                                self.fieldWidth,
                                                item['callback'])
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout


    def getChoiceWidget(self, name, item):
        layout = QHBoxLayout()
        label, widget = WidgetTool.getComboInput(self,
                                                 name+":",
                                                 item['choices'])
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout


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

