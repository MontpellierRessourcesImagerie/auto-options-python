from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from napari.utils.events import Event
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
        self.napariUtil = NapariUtil(self.viewer)
        self.imageLayers = self.napariUtil.getImageLayers()
        self.fftLayers = self.napariUtil.getFFTLayers()
        self.labelLayers = self.napariUtil.getLabelLayers()
        self.pointLayers = self.napariUtil.getPointsLayers()
        self.mainLayout = None
        self.imageComboBoxes = []
        self.fftComboBoxes = []
        self.labelComboBoxes = []
        self.pointComboBoxes = []
        self.widgets = {}
        self.viewer.layers.events.inserted.connect(self._onLayerAddedOrRemoved)
        self.viewer.layers.events.removed.connect(self._onLayerAddedOrRemoved)
        self.input_layer = None
        self.createLayout()


    def createLayout(self):
        self.mainLayout = QVBoxLayout()
        for name, item in self.options.items.items():
            widget = None
            activator = None
            if item['type'] == 'image':
                layout, widget, activator = self.getImageWidget(name, item)
                self.mainLayout.addLayout(layout)
                self.imageComboBoxes.append(widget)
            if item['type'] == 'fft':
                layout, widget, activator = self.getFFTWidget(name, item)
                self.mainLayout.addLayout(layout)
                self.fftComboBoxes.append(widget)
            if item['type'] == 'int':
                layout, widget, activator = self.getIntWidget(name, item)
                self.mainLayout.addLayout(layout)
            if item['type'] == 'float':
                layout, widget, activator = self.getFloatWidget(name, item)
                self.mainLayout.addLayout(layout)
            if item['type'] == 'choice':
                layout, widget, activator = self.getChoiceWidget(name, item)
                self.mainLayout.addLayout(layout)
            if item['type'] == 'str':
                layout, widget, activator = self.getStrWidget(name, item)
                self.mainLayout.addLayout(layout)
            if item['type'] == 'bool':
                layout, widget, activator = self.getBoolWidget(name, item)
                self.mainLayout.addLayout(layout)
            self.widgets[name] = widget
            if activator is not None:
                activator.stateChanged.connect(lambda _, cb=activator, n=name: self.options.items[n].__setitem__('activated', cb.isChecked()))
        self.setLayout(self.mainLayout)


    def getImageWidget(self, name, item):
        layout = QHBoxLayout()
        self.imageLayers = self.napariUtil.getImageLayers()
        label, widget, activator = WidgetTool.getComboInput(self,
                                                 labelText=name+":",
                                                 values=self.imageLayers,
                                                 activatable=item.get('activable', False),
                                                 activated=item.get('activated', True),
                                                 callback=None)
        if activator:
            layout.addWidget(activator)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget, activator


    def getFFTWidget(self, name, item):
        layout = QHBoxLayout()
        self.fftLayers = self.napariUtil.getFFTLayers()
        label, widget, activator = WidgetTool.getComboInput(self,
                                                 labelText=name+":",
                                                 values=self.fftLayers,
                                                 activatable=item.get('activable', False),
                                                 activated=item.get('activated', True),
                                                 callback=None)
        if activator:
            layout.addWidget(activator)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget, activator


    def getIntWidget(self, name, item):
        layout = QHBoxLayout()
        label, widget, activator = WidgetTool.getLineInput(self,
                                                labelText=name+":",
                                                defaultValue=item['value'],
                                                fieldWidth=self.fieldWidth,
                                                activatable=item.get('activable', False),
                                                activated=item.get('activated', True),
                                                callback=item['callback'])
        if activator:
            layout.addWidget(activator)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget, activator


    def getFloatWidget(self, name, item):
        layout = QHBoxLayout()
        label, widget, activator = WidgetTool.getLineInput(self,
                                                labelText=name+":",
                                                defaultValue=item['value'],
                                                fieldWidth=self.fieldWidth,
                                                activatable=item.get('activable', False),
                                                activated=item.get('activated', True),
                                                callback=item['callback'])
        if activator:
            layout.addWidget(activator)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget, activator


    def getStrWidget(self, name, item):
        layout = QHBoxLayout()
        label, widget, activator = WidgetTool.getLineInput(self,
                                                labelText=name+":",
                                                defaultValue=item['value'],
                                                fieldWidth=self.fieldWidth,
                                                activatable=item.get('activable', False),
                                                activated=item.get('activated', True),
                                                callback=item['callback'])
        
        if activator:
            layout.addWidget(activator)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget, activator


    def getChoiceWidget(self, name, item):
        layout = QHBoxLayout()
        label, widget, activator = WidgetTool.getComboInput(self,
                                                 labelText=name+":",
                                                 values=item['choices'],
                                                 activatable=item.get('activable', False),
                                                 activated=item.get('activated', True),
                                                 callback=item.get('callback', None))
        widget.setCurrentText(item['value'])
        if activator:
            layout.addWidget(activator)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget, activator


    def getBoolWidget(self, name, item):
        layout = QHBoxLayout()
        label, widget, activator = WidgetTool.getCheckbox(self,
                                                labelText=name+":",
                                                defaultValue=item['value'],
                                                fieldWidth=self.fieldWidth,
                                                activatable=item.get('activable', False),
                                                activated=item.get('activated', True),
                                                callback=item['callback'])
        if activator:
            layout.addWidget(activator)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget, activator


    def addApplyButton(self, callback):
        applyButton = QPushButton("Apply")
        self.mainLayout.addWidget(applyButton)
        applyButton.clicked.connect(self._onApplyButtonClicked)
        applyButton.clicked.connect(callback)


    def _onApplyButtonClicked(self):
        self.transferValues()
        self.options.save()
        self.options.load()


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
        for name, item in self.options.items.items():
            widget = self.widgets[name]
            if item['type']  in ['image', 'choice', 'fft']:
                text = widget.currentText()
                item['value'] = text
            if item['type'] == 'int':
                item['value'] = int(widget.text().strip())
            if item['type'] == 'float':
                item['value'] = float(widget.text().strip())
            if item['type'] == 'str':
                item['value'] = widget.text()
                print(item['value'])
            if item['type'] == 'bool':
                item['value'] = widget.isChecked()


    def ignoreChange(self):
        pass


    def _onLayerAddedOrRemoved(self, event: Event):
        self.updateLayerSelectionComboBoxes()


    def updateLayerSelectionComboBoxes(self):
        imageLayers = self.napariUtil.getImageLayers()
        labelLayers = self.napariUtil.getLabelLayers()
        pointLayers = self.napariUtil.getPointsLayers()
        fftLayers = self.napariUtil.getFFTLayers()
        for comboBox in self.imageComboBoxes:
            WidgetTool.replaceItemsInComboBox(comboBox, imageLayers)
        for comboBox in self.labelComboBoxes:
            WidgetTool.replaceItemsInComboBox(comboBox, labelLayers)
        for comboBox in self.pointComboBoxes:
            WidgetTool.replaceItemsInComboBox(comboBox, pointLayers)
        for comboBox in self.fftComboBoxes:
            WidgetTool.replaceItemsInComboBox(comboBox, fftLayers)


    def getImageLayer(self, name):
        layer = self.napariUtil.getLayerWithName(self.options.get(name)['value'])
        return layer
    

    def getCurrentImageLayer(self):
        return self.napariUtil.getCurrentImageLayer()
    

    def getCurrentShapesLayer(self):
        return self.napariUtil.getCurrentShapesLayer()
    

    def getCurrentPointsLayer(self):
        return self.napariUtil.getCurrentPointsLayer()
    

    def getCurrentLabelsLayer(self):
        return self.napariUtil.getCurrentLabelsLayer()