from qtpy.QtWidgets import (
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton,
    QGridLayout,
    QWidget,
    QLabel
)
from qtpy.QtGui import QColor
from napari.utils.events import Event

from autooptions.qtutil import WidgetTool
from autooptions.napari_util import NapariUtil
from autooptions.layouts import LayoutFactory


class OptionsWidget(QWidget):
    """
    Automatically creates a widget from an options object. The option values can be changed in the dialog.
    When the 'Apply' or the 'OK' button is pressed the values are copied from the dialog to the options object and saved
    to the options file.
    """

    def __init__(self, viewer, options, layout_type='default', client=None, sameRowSet=None):
        """
        Create a new options widget. Layer add and remove events are caught and
        the combo-boxes are updated accordingly, depending on the layer types.

        :param viewer: The napari viewer
        :param options: The options from which the dialog is created
        :param client: The client that handles callbacks when option values change
        :param sameRowSet: A set of widgets that should be placed on the same row as the last added widget.
        """
        super().__init__()
        self.setWindowTitle(options.optionsName)
        self.viewer = viewer
        self.client = client
        self.options = options
        self.napariUtil = NapariUtil(self.viewer)
        self.imageLayers = self.napariUtil.getImageLayers()
        self.fftLayers = self.napariUtil.getFFTLayers()
        self.labelLayers = self.napariUtil.getLabelLayers()
        self.pointLayers = self.napariUtil.getPointsLayers()
        self.buttonsLayout = None
        self.buttons = {}
        self.imageComboBoxes = []
        self.fftComboBoxes = []
        self.labelComboBoxes = []
        self.pointComboBoxes = []
        self.widgets = {}
        self.sameRowSet = set() if sameRowSet is None else sameRowSet.copy()
        self.viewer.layers.events.inserted.connect(self._onLayerAddedOrRemoved)
        self.viewer.layers.events.removed.connect(self._onLayerAddedOrRemoved)
        self.mainLayout = None
        self._createLayout(layout_type)


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
        self.buttons['OK'] = button
        self._getButtonsLayout().addWidget(button)


    def addCancelButton(self, callback):
        """
        Add a cancel button to the options widget. When the button is pressed the dialog is closed, the values in the
        dialog are not copied to the options object.

        :param callback: The client can register a callback that is called when the cancel button is pressed
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
        if 'OK' in self.buttons.keys():
            return self.buttons['OK']
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
        opt = self.options.get(name)
        return None if opt is None else self.napariUtil.getLayerWithName(opt['value'])


    def _callbackFor(self, name):
        func = None
        if self.client and name:
            func = getattr(self.client, name)
        return func
    

    def sameRow(self, name):
        self.sameRowSet.add(name)

    
    def isSameRow(self, name):
        return name in self.sameRowSet
    

    def _createLayout(self, layout_type):
        self.mainLayout = LayoutFactory.createLayout(layout_type=layout_type, same_row_set=self.sameRowSet, parent=self)
        for name, item in self.options.items.items():
            widget = None
            if item['type'] == 'image':
                checkbox, widget = self._getImageWidget(name, item)
                self.imageComboBoxes.append(widget)
            if item['type'] == 'labels':
                checkbox, widget = self._getLabelsWidget(name, item)
                self.labelComboBoxes.append(widget)
            if item['type'] == 'points':
                checkbox, widget = self._getPointsWidget(name, item)
                self.pointComboBoxes.append(widget)
            if item['type'] == 'fft':
                checkbox, widget = self._getFFTWidget(name, item)
                self.fftComboBoxes.append(widget)
            if item['type'] == 'int':
                checkbox, widget = self._getIntWidget(name, item)
            if item['type'] == 'float':
                checkbox, widget = self._getFloatWidget(name, item)
            if item['type'] == 'choice':
                checkbox, widget = self._getChoiceWidget(name, item)
            if item['type'] == 'str':
                checkbox, widget = self._getStrWidget(name, item)
            if item['type'] == 'bool':
                checkbox, widget = self._getBoolWidget(name, item)
            if item['type'] == 'folder':
                checkbox, widget = self._getFolderWidget(name, item)
            if item['type'] == 'file':
                checkbox, widget = self._getFileWidget(name, item)
            self.widgets[name] = (checkbox, widget)
        self.setLayout(self.mainLayout)

    
    def _getFolderWidget(self, name, item):
        label, widget, btn, active = WidgetTool.getDiskIoInput(
                                                    f"{name}:",
                                                    item['value'],
                                                    object='folder',
                                                    callback=self._callbackFor(item['callback']),
                                                    optional=item['optional']
                                                )

        self.mainLayout.addToLayout(
            name=name,
            optionalCheckbox=active, 
            nameLabel=label, 
            valueField=widget, 
            tailWidget=btn
        )
        
        return active, widget
    

    def _getFileWidget(self, name, item):
        label, widget, btn, active = WidgetTool.getDiskIoInput(
                                                    f"{name}:",
                                                    item['value'],
                                                    object='file',
                                                    callback=self._callbackFor(item['callback']),
                                                    optional=item['optional']
                                                )
        self.mainLayout.addToLayout(
            name=name,
            optionalCheckbox=active,
            nameLabel=label,
            valueField=widget,
            tailWidget=btn
        )

        return active, widget


    def _getImageWidget(self, name, item):
        self.imageLayers = self.napariUtil.getImageLayers()
        label, widget, active = WidgetTool.getComboInput(
                                                    f"{name}:",
                                                    self.imageLayers,
                                                    callback=self._callbackFor(item['callback']),
                                                    optional=item['optional']
                                                )

        self.mainLayout.addToLayout(
            name=name,
            optionalCheckbox=active,
            nameLabel=label,
            valueField=widget
        )

        return active, widget


    def _getLabelsWidget(self, name, item):
        self.labelLayers = self.napariUtil.getLabelLayers()
        label, widget, active = WidgetTool.getComboInput(
                                                    f"{name}:",
                                                    self.labelLayers,
                                                    callback=self._callbackFor(item['callback']),
                                                    optional=item['optional']
                                                )
        
        self.mainLayout.addToLayout(
            name=name,
            optionalCheckbox=active,
            nameLabel=label,
            valueField=widget
        )

        return active, widget


    def _getPointsWidget(self, name, item):
        self.pointsLayers = self.napariUtil.getPointsLayers()
        label, widget, active = WidgetTool.getComboInput(
                                                    f"{name}:",
                                                    self.pointsLayers,
                                                    callback=self._callbackFor(item['callback']),
                                                    optional=item['optional']
                                                )
        
        self.mainLayout.addToLayout(
            name=name,
            optionalCheckbox=active,
            nameLabel=label,
            valueField=widget
        )

        return active, widget


    def _getFFTWidget(self, name, item):
        self.fftLayers = self.napariUtil.getFFTLayers()
        label, widget, active = WidgetTool.getComboInput(
                                                    f"{name}:",
                                                    self.fftLayers,
                                                    callback=self._callbackFor(item['callback']),
                                                    optional=item['optional']
                                                )
        
        self.mainLayout.addToLayout(
            name=name,
            optionalCheckbox=active,
            nameLabel=label,
            valueField=widget
        )

        return active, widget


    def _getIntWidget(self, name, item):
        label, widget, active = WidgetTool.getLineInput(
                                                f"{name}:",
                                                item['value'],
                                                callback=self._callbackFor(item['callback']),
                                                optional=item['optional']
                                            )
        
        self.mainLayout.addToLayout(
            name=name,
            optionalCheckbox=active,
            nameLabel=label,
            valueField=widget
        )

        return active, widget


    def _getFloatWidget(self, name, item):
        label, widget, active = WidgetTool.getLineInput(
                                                f"{name}:",
                                                item['value'],
                                                callback=self._callbackFor(item['callback']),
                                                optional=item['optional']
                                            )
        self.mainLayout.addToLayout(
            name=name,
            optionalCheckbox=active,
            nameLabel=label,
            valueField=widget
        )

        return active, widget


    def _getStrWidget(self, name, item):
        label, widget, active = WidgetTool.getLineInput(
                                                f"{name}:",
                                                item['value'],
                                                callback=self._callbackFor(item['callback']),
                                                optional=item['optional']
                                            )
        
        self.mainLayout.addToLayout(
            name=name,
            optionalCheckbox=active,
            nameLabel=label,
            valueField=widget
        )

        return active, widget


    def _getChoiceWidget(self, name, item):
        label, widget, active = WidgetTool.getComboInput(
                                                f"{name}:",
                                                item['choices'],
                                                callback=self._callbackFor(item['callback']),
                                                optional=item['optional']
                                            )
        widget.setCurrentText(item['value'])
        
        self.mainLayout.addToLayout(
            name=name,
            optionalCheckbox=active,
            nameLabel=label,
            valueField=widget
        )

        return active, widget


    def _getBoolWidget(self, name, item):
        label, widget, active = WidgetTool.getCheckbox(
                                                f"{name}:",
                                                item['value'],
                                                callback=self._callbackFor(item['callback']),
                                                optional=item['optional']
                                            )
        
        self.mainLayout.addToLayout(
            name=name,
            optionalCheckbox=active,
            nameLabel=label,
            valueField=widget
        )

        return active, widget


    def _getButtonsLayout(self):
        if not self.buttonsLayout:
            self.buttonsLayout = QHBoxLayout()
            self.mainLayout.addSpacing(15)
            self.mainLayout.addLayout(self.buttonsLayout)
        return self.buttonsLayout


    def _createApplyButton(self, callback):
        button = self._createButton("&Apply", callback, self._onApplyButtonClicked)
        return button


    def _createOKButton(self, callback):
        button = self._createButton("&OK", callback, self._onOKButtonClicked)
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
            checkbox, widget = self.widgets[name]
            isEnabled = checkbox.isChecked() if checkbox else True
            if not isEnabled:
                item['value'] = None
                continue
            if item['type']  in ['image', 'choice', 'fft']:
                text = widget.currentText()
                item['value'] = text
            if item['type'] == 'int':
                text = widget.text().strip()
                item['value'] = int(text) if text else 0
            if item['type'] == 'float':
                text = widget.text().strip()
                item['value'] = float(text) if text else 0.0
            if item['type'] == 'str':
                item['value'] = widget.text()
            if item['type'] == 'bool':
                item['value'] = widget.isChecked()
            if item['type'] == 'folder' or item['type'] == 'file':
                item['value'] = widget.text()


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


