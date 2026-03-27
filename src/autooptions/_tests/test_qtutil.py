from qtpy.QtWidgets import QWidget
from autooptions.qtutil import WidgetTool
from autooptions.qtutil import TableView



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
    assert COUNTER_TEXT_CHANGED == 0
    assert inputWidget.text() == str(10)
    inputWidget.setText("20")
    assert COUNTER_TEXT_CHANGED == 1
    assert inputWidget.maximumWidth() == 50



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