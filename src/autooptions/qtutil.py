import pyperclip
import numpy as np
import matplotlib.pyplot as plt
from qtpy.QtWidgets import (
    QHBoxLayout, 
    QCheckBox, 
    QWidget, 
    QVBoxLayout, 
    QLabel, 
    QLineEdit, 
    QComboBox, 
    QTableWidget, 
    QTableWidgetItem, 
    QAction,
    QFileDialog,
    QPushButton,
    QSizePolicy
)
from qtpy.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from napari.utils import notifications
from autooptions.array_util import ArrayUtil

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import napari


class WidgetTool:
    """
    Utility methods for working with qt-widgets.
    """

    @staticmethod
    def activateWidgetFactory(widget):
        def activateWidget(state):
            widget.setEnabled(state == 2)
        return activateWidget

    @staticmethod
    def _makeActivable(widgets, optional):
        isOptional, isActive = optional
        if not isOptional:
            return None
        checkbox = QCheckBox()
        checkbox.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        checkbox.setChecked(isActive)
        for widget in widgets:
            checkbox.stateChanged.connect(WidgetTool.activateWidgetFactory(widget))
            if not isActive:
                widget.setEnabled(False)
        return checkbox

    @staticmethod
    def _makeLabel(labelText):
        label = QLabel()
        label.setText(labelText)
        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        return label

    @staticmethod
    def getLineInput(labelText, defaultValue, callback=None, optional=(False, True)):
        """Returns a label displaying the given text and an input field
        with the given default value.

        :param labelText: The text of the label
        :param defaultValue: The value initailly displayed in the input field
        :param callback: A callback function with a parameter text. The function
                         is called with the new text when the content of the
                         input field changes
        :return: A tuple of the label and the input field
        :rtype: (QLabel, QLineEdit)
        """
        label = WidgetTool._makeLabel(labelText)
        inputWidget = QLineEdit()
        inputWidget.setText(str(defaultValue))
        if callback:
            inputWidget.textEdited.connect(callback)
        inputWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        cb_used = WidgetTool._makeActivable([label, inputWidget], optional)
        return label, inputWidget, cb_used
    
    @staticmethod
    def _browseFolder(inputWidget, callback):
        folder = QFileDialog.getExistingDirectory(None, "Select Folder")
        if folder:
            inputWidget.setText(folder)
            if callback:
                callback(folder)

    @staticmethod
    def _browseFile(inputWidget, callback):
        file, _ = QFileDialog.getOpenFileName(None, "Select File")
        if file:
            inputWidget.setText(file)
            if callback:
                callback(file)
    

    @staticmethod
    def getDiskIoInput(labelText, defaultValue, object, callback=None, optional=(False, True)):
        """
        Returns a label displaying the given text, an input field with the given default value and a button to browse for a file or folder.

        :param labelText: The text of the label
        :param defaultValue: The value initailly displayed in the input field
        :param object: A string that is either 'file' or 'folder' and determines whether the input field is for a file or a folder.
        :param callback: A callback function with a parameter text. The function
                         is called with the new text when the content of the
                         input field changes
        :param optional: A tuple of two booleans. The first boolean determines whether the input field is optional. The second boolean determines whether the input field is active if it is optional.
        :return: A tuple of the label, the input field and the button
        :rtype: (QLabel, QLineEdit, QPushButton)
        """
        label = WidgetTool._makeLabel(labelText)
        inputWidget = QLineEdit()
        inputWidget.setText(str(defaultValue))
        if callback:
            inputWidget.textEdited.connect(callback)
        inputWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        button = QPushButton("📁")
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        fx = WidgetTool._browseFolder if object == 'folder' else WidgetTool._browseFile
        button.clicked.connect(lambda: fx(inputWidget, callback))
        cb_used = WidgetTool._makeActivable([label, inputWidget, button], optional)
        
        return label, inputWidget, button, cb_used


    @staticmethod
    def getComboInput(labelText, values, callback=None, optional=(False, True)):
        """Returns a label displaying the given text and a combo-box
        with the given values.

        :param labelText: The text of the label
        :param values: The values in the list of the combo-box
        :param callback: A callback function that is called with the new text when the selected text changes.
        :param optional: A tuple of two booleans. The first boolean determines whether the input field is optional. The second boolean determines whether the input field is active if it is optional.
        :return: A tuple of the label and the input field
        :rtype: (QLabel, QComboBox)
        """
        label = WidgetTool._makeLabel(labelText)
        inputCombo = QComboBox()
        inputCombo.addItems(values)
        inputCombo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        if callback:
            inputCombo.currentTextChanged.connect(callback)
        cb_used = WidgetTool._makeActivable([label, inputCombo], optional)
        return label, inputCombo, cb_used


    @staticmethod
    def replaceItemsInComboBox(comboBox, newItems):
        """Replace the items in the combo-box with newItems

        :param comboBox: The combo-box in which the items will be replaced
        :param newItems: The new items that will replace the current items
                         in the combo-box.
        """
        selectedText = comboBox.currentText()
        comboBox.clear()
        comboBox.addItems(newItems)
        index = -1
        try:
            index = newItems.index(selectedText)
        except ValueError:
            index = -1
        if index > -1:
            comboBox.setCurrentIndex(index)


    @staticmethod
    def getCheckbox(labelText, defaultValue, callback=None, optional=(False, True)):
        """Answers a label and a checkbox checked or unchecked depeding on the default value.

        :param labelText: The text of the label
        :param defaultValue: The boolean default value
        :param callback: A callback function
        :param optional: A tuple of two booleans. The first boolean determines whether the input field is optional. The second boolean determines whether the input field is active if it is optional.
        :return: A tuple of a label and a checkbox
        """
        label = WidgetTool._makeLabel(labelText)
        cb = QCheckBox()
        cb.setChecked(defaultValue)
        if callback:
            cb.stateChanged.connect(callback)
        cb.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        cb_used = WidgetTool._makeActivable([label, cb], optional)
        return label, cb, cb_used



class TableView(QTableWidget):
    """ 
    A table that allows to copy the selected cells to the system-clipboard.
    """

    def __init__(self, data, *args):
        """Create a new table from data.

        :param data: A dictionary with the column names as keys and the data
        in the columns as lists.
        """
        rows = 0
        columns = 0
        if data:
            columns = len(data)
            rows = len(list(data.values())[0])
        QTableWidget.__init__(self, rows, columns, *args)
        self.data = data
        if data:
            self.__setData()
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        copyAction = QAction("Copy\tCtrl+C", self)
        copyAction.triggered.connect(self.copyDataToClipboard)
        self.addAction(copyAction)
        self.resetAction = QAction("Reset", self)
        self.addAction(self.resetAction)
        self.deleteAction = QAction("Delete", self)
        self.addAction(self.deleteAction)


    def setData(self, table):
        """Clear the table and replace the data in the table with the input table"""
        self.data = table
        self.resetView()


    def resetView(self):
        """Resets the view to the data of the table view"""
        self.clear()
        self.__setData()


    def __setData(self):
        horizontalHeaders = []
        for n, key in enumerate(self.data.keys()):
            horizontalHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newItem = QTableWidgetItem(str(item))
                newItem.setTextAlignment(Qt.AlignRight)
                self.setItem(m, n, newItem)
        self.setHorizontalHeaderLabels(horizontalHeaders)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()


    def keyPressEvent(self, event):
        """Copy the selected table data to the system clipboard if the key-event
        is ctrl+C.

        :param event: The received key-pressed event.
        """
        super().keyPressEvent(event)
        if event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):
            self.copyDataToClipboard()


    def copyDataToClipboard(self):
        """ Copy the data in the selected table-cells into the system clipboard.
        """
        notifications.show_info("copying data to clipboard")
        tableDataAsText = self.getSelectedDataAsString()
        pyperclip.copy(tableDataAsText)


    def getSelectedDataAsString(self):
        """ Get the data in the selected cells as a string. Columns are
        separated by tabs and lines by newlines".
        """
        copied_cells = self.selectedIndexes()
        if len(copied_cells) == 0:
            return ""
        labels = [self.horizontalHeaderItem(id).text() for id in range(0, self.columnCount())]
        data = [['' for i in range(self.columnCount())] for j in range(self.rowCount())]
        for cell in copied_cells:
            data[cell.row()][cell.column()] = cell.data()
        table =  np.array(data)
        table, columnIndices, _ = ArrayUtil.stripZeroRowsAndColumns(table, zero='')
        lines = ''
        for row in table:
            lines = lines + "\t".join([str(elem) for elem in row]) + "\n"
        lines = lines[:-1]
        remainingHeadings = [labels[index] for index in columnIndices]
        result = "\t".join(remainingHeadings) + "\n" + lines
        return result



class PlotWidget(QWidget):
    """
    A widget that contains a pyplot plot.
    """

    def __init__(self, viewer: "napari.viewer.Viewer"):
        """Create a new empty plot widget.

            param viewer: The napari viewer in which the widget will be displayed
        """
        super().__init__()
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.viewer = viewer
        self.createLayout()
        self.formatStrings = []
        self.title = "Plot"
        self.X = []
        self.Y = []
        self.area = 'left'
        self.tabify = True
        self.xLabel = "x"
        self.yLabel = "y"


    def createLayout(self):
        """Create the layout of the widget.
        """
        mainLayout = QVBoxLayout()
        canvasLayout = QHBoxLayout()
        canvasLayout.addWidget(self.canvas)
        mainLayout.addLayout(canvasLayout)
        self.setLayout(mainLayout)


    def addData(self, X, Y, formatString=None):
        """Add the data and the format string.
        """
        self.X.append(X)
        self.Y.append(Y)
        if formatString:
            self.formatStrings.append(formatString)


    def clear(self):
        """Remove everything from the plot.
        """
        self.figure.clear()


    def display(self):
        """Display the plot as a dock widget in napari.
        """
        self.ax.set_xlabel(self.xLabel)
        self.ax.set_ylabel(self.yLabel)
        if self.formatStrings:
            for x, y, plotFormat in zip(self.X, self.Y, self.formatStrings):
                self.ax.plot(x, y, plotFormat)
        else:
            for x, y in zip(self.X, self.Y):
                self.ax.plot(x, y)
        self.canvas.draw()
        self.viewer.window.add_dock_widget(self, area=self.area, name=self.title, tabify=self.tabify)

