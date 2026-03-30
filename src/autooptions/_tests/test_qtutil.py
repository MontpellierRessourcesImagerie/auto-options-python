import pyperclip
from qtpy.QtWidgets import QWidget
from qtpy.QtGui import QKeyEvent
from qtpy.QtCore import QEvent
from qtpy.QtCore import Qt
from autooptions.qtutil import WidgetTool
from autooptions.qtutil import TableView
from autooptions.qtutil import PlotWidget



COUNTER_TEXT_CHANGED = 0
COUNTER_CHECKBOX_CHANGED = 0



class ParentWidget(QWidget):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")



def handleTextChanged(text):
    global COUNTER_TEXT_CHANGED
    COUNTER_TEXT_CHANGED = COUNTER_TEXT_CHANGED + 1



def handleRemoveBackgroundChanged(value):
    global COUNTER_CHECKBOX_CHANGED
    COUNTER_CHECKBOX_CHANGED = COUNTER_CHECKBOX_CHANGED + 1



def testGetLineInput(make_napari_viewer_proxy):
    make_napari_viewer_proxy()
    parent = ParentWidget()
    label, inputWidget = WidgetTool.getLineInput(parent,
                                            "your guess",
                                            10,
                                            50,
                                            handleTextChanged)
    assert label in parent.children()
    assert inputWidget in parent.children()
    assert label.parent() == parent
    assert inputWidget.parent() == parent
    assert label.text() == "your guess"
    counter = COUNTER_TEXT_CHANGED
    assert inputWidget.text() == str(10)
    inputWidget.setText("20")
    assert COUNTER_TEXT_CHANGED == counter  # Only editing in the interface sends the signal,
                                            # not programmatically changing the value
    assert inputWidget.maximumWidth() == 50


def testGetLineInputNoCallback(make_napari_viewer_proxy):
    make_napari_viewer_proxy()
    parent = ParentWidget()
    label, inputWidget = WidgetTool.getLineInput(parent,
                                            "your guess",
                                            10,
                                            50,
                                            None)
    assert label in parent.children()
    assert inputWidget in parent.children()
    assert label.parent() == parent
    assert inputWidget.parent() == parent
    assert label.text() == "your guess"
    counter = COUNTER_TEXT_CHANGED
    assert inputWidget.text() == str(10)
    inputWidget.setText("20")
    assert inputWidget.maximumWidth() == 50
    assert COUNTER_TEXT_CHANGED == counter


def testGetComboBox(make_napari_viewer_proxy):
    make_napari_viewer_proxy()
    parent = ParentWidget()
    label, comboWidget = WidgetTool.getComboInput(parent,
                                                  "fruits",

                                                  ["apple", "orange", "banana"])
    assert label in parent.children()
    assert comboWidget in parent.children()
    assert label.parent() == parent
    assert comboWidget.parent() == parent
    assert label.text() == "fruits"
    allItems = [comboWidget.itemText(i) for i in range(comboWidget.count())]
    assert allItems == ["apple", "orange", "banana"]



def testReplaceItemsInComboBox(make_napari_viewer_proxy):
    make_napari_viewer_proxy()
    parent = ParentWidget()
    label, comboWidget = WidgetTool.getComboInput(parent,
                                                  "fruits",
                                                  ["apple", "orange", "banana"])
    WidgetTool.replaceItemsInComboBox(comboWidget, ["lemon", "ananas"])
    allItems = [comboWidget.itemText(i) for i in range(comboWidget.count())]
    assert allItems == ["lemon", "ananas"]
    assert comboWidget.currentText() == "lemon"
    comboWidget.setCurrentIndex(1)
    WidgetTool.replaceItemsInComboBox(comboWidget, ["apple", "ananas"])
    allItems = [comboWidget.itemText(i) for i in range(comboWidget.count())]
    assert allItems == ["apple", "ananas"]
    assert comboWidget.currentText() == "ananas"



def testGetCheckBox(make_napari_viewer_proxy):
    make_napari_viewer_proxy()
    parent = ParentWidget()
    label, checkbox = WidgetTool.getCheckbox(parent,
                                             "remove background",
                                             True,
                                             50,
                                             handleRemoveBackgroundChanged)
    assert label in parent.children()
    assert checkbox in parent.children()
    assert checkbox.parent() == parent
    assert label.parent() == parent
    assert label.text() == "remove background"
    assert checkbox.isChecked()
    assert checkbox.maximumWidth() == 50
    checkbox.setChecked(False)
    assert COUNTER_CHECKBOX_CHANGED == 1
    label2, checkbox2 = WidgetTool.getCheckbox(parent,
                                             "smooth",
                                             False,
                                             50,
                                             None)
    assert not checkbox2.isChecked()



class TestTableView:


    def testConstructor(self, make_napari_viewer_proxy):
        make_napari_viewer_proxy()
        table = {"area": [23.87, 65.28, 12.98], "mean": [19992, 2233, 24553]}
        tableView = TableView(table)
        assert tableView.data == table
        tableView2 = TableView(None)
        assert not tableView2.data


    def testSetData(self, make_napari_viewer_proxy):
        make_napari_viewer_proxy()
        table = {"area": [23.87, 65.28, 12.98], "mean": [19992, 2233, 24553]}
        table2 = {"fruits": ["apple", "orange", "banana"], "animals": ["lion", "tiger"]}
        tableView = TableView(table)
        tableView.setData(table2)
        assert tableView.data == table2


    def testResetView(self, make_napari_viewer_proxy):
        make_napari_viewer_proxy()
        table = {"area": [23.87, 65.28, 12.98], "mean": [19992, 2233, 24553]}
        tableView = TableView(table)
        tableView.resetView()
        assert tableView.data == table


    def testKeyPressEvent(self, make_napari_viewer_proxy):
        pyperclip.copy("")
        make_napari_viewer_proxy()
        table = {"area": [23.87, 65.28, 12.98], "mean": [19992, 2233, 24553]}
        tableView = TableView(table)
        tableView.selectAll()
        event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_C, Qt.KeyboardModifier.ControlModifier, "copy")
        tableView.keyPressEvent(event)
        text = pyperclip.paste()
        assert "23.87" in text
        assert "24553" in text


    def testKeyPressEventNoCopy(self, make_napari_viewer_proxy):
        pyperclip.copy("")
        make_napari_viewer_proxy()
        table = {"area": [23.87, 65.28, 12.98], "mean": [19992, 2233, 24553]}
        tableView = TableView(table)
        tableView.selectAll()
        event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_C, Qt.KeyboardModifier.ShiftModifier, "copy")
        tableView.keyPressEvent(event)
        text = pyperclip.paste()
        assert text == ""


    def testCopyDataToClipboard(self, make_napari_viewer_proxy):
        pyperclip.copy("")
        make_napari_viewer_proxy()
        table = {"area": [23.87, 65.28, 12.98], "mean": [19992, 2233, 24553]}
        tableView = TableView(table)
        tableView.copyDataToClipboard()
        text = pyperclip.paste()
        assert text == ""
        tableView.selectAll()
        tableView.copyDataToClipboard()
        text = pyperclip.paste()
        assert "23.87" in text
        assert "24553" in text


class TestPlotWidget:


    def testConstructor(self, make_napari_viewer_proxy):
        viewer = make_napari_viewer_proxy()
        plot = PlotWidget(viewer)
        assert plot.figure
        assert plot.X == []
        assert plot.Y == []


    def testAddData(self, make_napari_viewer_proxy):
        viewer = make_napari_viewer_proxy()
        plot = PlotWidget(viewer)
        plot.addData([1, 2, 3], [1, 4, 9], "r+")
        assert [1, 2, 3] in plot.X
        assert [1, 4, 9] in plot.Y
        assert "r+" in plot.formatStrings


    def testClearData(self, make_napari_viewer_proxy):
        viewer = make_napari_viewer_proxy()
        plot = PlotWidget(viewer)
        plot.addData([1, 2, 3], [1, 4, 9], "r+")
        plot.clear()
        assert True


    def testDisplay(self, make_napari_viewer_proxy):
        viewer = make_napari_viewer_proxy()
        plot = PlotWidget(viewer)
        plot.addData([1, 2, 3], [1, 4, 9], "r+")
        plot.display()
        assert plot.ax.get_xlabel() == plot.xLabel
        assert plot.ax.get_ylabel() == plot.yLabel
        plot2 = PlotWidget(viewer)
        plot2.addData([1, 2, 3], [1, 4, 9])
        plot2.display()
        assert plot2.ax.get_xlabel() == plot2.xLabel
        assert plot2.ax.get_ylabel() == plot2.yLabel

