from qtpy.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from napari.utils.events import Event
from qtpy.QtWidgets import QWidget
from autooptions.qtutil import WidgetTool
from autooptions.napari_util import NapariUtil



class OptionsWidget(QWidget):
    """
    Automatically creates a widget from an options object. The option values can be changed in the dialog.
    When the Apply or the Ok-button is pressed the values are copied from the dialog to the options object and saved
    to the options file.
    """

    def __init__(self, viewer, options, client=None, sameRowMap=None):
        """
        Create a new options widget. Layer add and remove events are caught and
        the combo-boxes are updated accordingly, depending on the layer types.

        :param viewer: The napari viewer
        :param options: The options from which the dialog is created
        :param client: The client that handles callbacks when option values change
        """
        super().__init__()
        self.setWindowTitle(options.optionsName)
        self.viewer = viewer
        self.client = client
        self.options = options
        self.fieldWidth = 50
        self.napariUtil = NapariUtil(self.viewer)
        self.imageLayers = self.napariUtil.getImageLayers()
        self.fftLayers = self.napariUtil.getFFTLayers()
        self.labelLayers = self.napariUtil.getLabelLayers()
        self.pointLayers = self.napariUtil.getPointsLayers()
        self.mainLayout = None
        self.buttonsLayout = None
        self.buttons = {}
        self.imageComboBoxes = []
        self.fftComboBoxes = []
        self.labelComboBoxes = []
        self.pointComboBoxes = []
        self.widgets = {}
        self._isSameRow = sameRowMap
        self.viewer.layers.events.inserted.connect(self._onLayerAddedOrRemoved)
        self.viewer.layers.events.removed.connect(self._onLayerAddedOrRemoved)
        self.input_layer = None
        self._createLayout()


    def addApplyButton(self, callback):
        """
        Add an apply button to the options widget. When the button is pressed the value are copied from the dialog
        to the options object. The dialog remains open.

        :param callback: The client can register a callback that is called when the apply button is pressed
        """
        button = self._createApplyButton(callback)
        self.buttons['Apply'] = button
        self._getButtonsLayout().addWidget(button)


    def addOKButton(self, callback):
        """
        Add an ok button to the options widget. When the button is pressed the value are copied from the dialog
        to the options object. The dialog is closed.

        :param callback: The client can register a callback that is called when the ok button is pressed
        """
        button = self._createOKButton(callback)
        self.buttons['Ok'] = button
        self._getButtonsLayout().addWidget(button)


    def addCancelButton(self, callback):
        """
        Add a cancel button to the options widget. When the button is pressed the dialog is closed, the values in the
        dialog are not copied to the options object.

        :param callback: The client can register a callback that is called when the ok button is pressed
        """
        button = self._createCancelButton(callback)
        self.buttons['Cancel'] = button
        self._getButtonsLayout().addWidget(button)


    def getApplyButton(self):
        """
        Answers the apply button if it exists and None otherwise.
        """
        if 'Apply' in self.buttons.keys():
            return self.buttons['Apply']
        return None


    def getOKButton(self):
        """
        Answers the ok button if it exists and None otherwise.
        """
        if 'Ok' in self.buttons.keys():
            return self.buttons['Ok']
        return None


    def getCancelButton(self):
        """
        Answers the cancel button if it exists and None otherwise.
        """
        if 'Cancel' in self.buttons.keys():
            return self.buttons['Cancel']
        return None


    def shut(self):
        """
        Shut down the options widget. Removes the dock-widget from the window and closes the widget.
        """
        self.viewer.window.remove_dock_widget(self)
        self.close()


    def getImageLayer(self, name):
        """
        Answer the image layer that has the name of the value of the option with the given name. The option must be
        a layer selection option (image, labels, points, fft).

        :param name: The name of an option
        :return: The layer that has the name corresponding to the value of the option
        """
        layer = self.napariUtil.getLayerWithName(self.options.get(name)['value'])
        return layer


    def _callbackFor(self, name):
        func = None
        if self.client and name:
            func = getattr(self.client, name)
        return func


    def sameRow(self, name):
        if self._isSameRow is None:
            self._isSameRow = {}
        self._isSameRow[name] = True


    def isSameRow(self, name):
        if self._isSameRow is None:
            return False
        if name in self._isSameRow.keys():
            return self._isSameRow[name]
        return False


    def _createLayout(self):
        self.mainLayout = QVBoxLayout()
        layout = None
        lastLayout = None
        for name, item in self.options.items.items():
            widget = None
            if item['type'] == 'image':
                layout, widget = self._getImageWidget(name, item)
                self.imageComboBoxes.append(widget)
            if item['type'] == 'labels':
                layout, widget = self._getLabelsWidget(name, item)
                self.labelComboBoxes.append(widget)
            if item['type'] == 'points':
                layout, widget = self._getPointsWidget(name, item)
                self.pointComboBoxes.append(widget)
            if item['type'] == 'fft':
                layout, widget = self._getFFTWidget(name, item)
                self.fftComboBoxes.append(widget)
            if item['type'] == 'int':
                layout, widget = self._getIntWidget(name, item)
            if item['type'] == 'float':
                layout, widget = self._getFloatWidget(name, item)
            if item['type'] == 'choice':
                layout, widget = self._getChoiceWidget(name, item)
            if item['type'] == 'str':
                layout, widget = self._getStrWidget(name, item)
            if item['type'] == 'bool':
                layout, widget = self._getBoolWidget(name, item)
            if self.isSameRow(name):
                lastLayout.addWidget(layout.itemAt(0).widget())
                lastLayout.addWidget(layout.itemAt(1).widget())
            else:
                self.mainLayout.addLayout(layout)
            self.widgets[name] = widget
            lastLayout = layout
        self.setLayout(self.mainLayout)


    def _getImageWidget(self, name, item):
        layout = QHBoxLayout()
        self.imageLayers = self.napariUtil.getImageLayers()
        label, widget = WidgetTool.getComboInput(self,
                                                 name +":",
                                                 self.imageLayers,
                                                 callback=self._callbackFor(item['callback']))
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget


    def _getLabelsWidget(self, name, item):
        layout = QHBoxLayout()
        self.labelLayers = self.napariUtil.getLabelLayers()
        label, widget = WidgetTool.getComboInput(self,
                                                 name +":",
                                                 self.labelLayers,
                                                 callback=self._callbackFor(item['callback']))
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget


    def _getPointsWidget(self, name, item):
        layout = QHBoxLayout()
        self.pointsLayers = self.napariUtil.getPointsLayers()
        label, widget = WidgetTool.getComboInput(self,
                                                 name +":",
                                                 self.pointsLayers,
                                                 callback=self._callbackFor(item['callback']))
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget


    def _getFFTWidget(self, name, item):
        layout = QHBoxLayout()
        self.fftLayers = self.napariUtil.getFFTLayers()
        label, widget = WidgetTool.getComboInput(self,
                                                 name +":",
                                                 self.fftLayers,
                                                 callback=self._callbackFor(item['callback']))
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget


    def _getIntWidget(self, name, item):
        layout = QHBoxLayout()
        label, widget = WidgetTool.getLineInput(self,
                                                name +":",
                                                item['value'],
                                                self.fieldWidth,
                                                self._callbackFor(item['callback']))
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget


    def _getFloatWidget(self, name, item):
        layout = QHBoxLayout()
        label, widget = WidgetTool.getLineInput(self,
                                                name +":",
                                                item['value'],
                                                self.fieldWidth,
                                                self._callbackFor(item['callback']))
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget


    def _getStrWidget(self, name, item):
        layout = QHBoxLayout()
        label, widget = WidgetTool.getLineInput(self,
                                                name +":",
                                                item['value'],
                                                self.fieldWidth,
                                                self._callbackFor(item['callback']))
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget


    def _getChoiceWidget(self, name, item):
        layout = QHBoxLayout()
        label, widget = WidgetTool.getComboInput(self,
                                                 name +":",
                                                 item['choices'],
                                                 callback=self._callbackFor(item['callback']))
        widget.setCurrentText(item['value'])
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget


    def _getBoolWidget(self, name, item):
        layout = QHBoxLayout()
        label, widget = WidgetTool.getCheckbox(self,
                                               name,
                                               item['value'],
                                               self.fieldWidth,
                                               self._callbackFor(item['callback']))
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout, widget

    def _getButtonsLayout(self):
        if not self.buttonsLayout:
            self.buttonsLayout = QHBoxLayout()
            self.mainLayout.addLayout(self.buttonsLayout)
        return self.buttonsLayout


    def _createApplyButton(self, callback):
        button = self._createButton("&Apply", callback, self._onApplyButtonClicked)
        return button


    def _createOKButton(self, callback):
        button = self._createButton("&Ok", callback, self._onOKButtonClicked)
        return button


    def _createCancelButton(self, callback):
        button = self._createButton("&Cancel", callback, self._onCancelButtonClicked)
        return button


    @classmethod
    def _createButton(cls, name, callback, innerCallback):
        button = QPushButton(name)
        button.clicked.connect(innerCallback)
        if callback:
            button.clicked.connect(callback)
        return button


    def _onApplyButtonClicked(self):
        self._transferValues()
        self.options.save()
        self.options.load()


    def _onOKButtonClicked(self):
        self._transferValues()
        self.options.save()
        self.options.load()
        self.shut()


    def _onCancelButtonClicked(self):
        self.shut()


    def _transferValues(self):
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
            if item['type'] == 'bool':
                item['value'] = widget.isChecked()


    def _onLayerAddedOrRemoved(self, event: Event):
        self._updateLayerSelectionComboBoxes()


    def _updateLayerSelectionComboBoxes(self):
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


