from qtpy.QtWidgets import (
    QHBoxLayout, 
    QGridLayout,
    QLabel
)

from autooptions.layouts.base_layout import BaseLayout

class GridLayout(BaseLayout):
    def __init__(self, same_row_set=None, parent=None):
        super().__init__(parent, same_row_set)
        self.gridLayout = QGridLayout()
        self.addLayout(self.gridLayout)
        self.columnIndex = 0
        self.nLines = 0
        self.setSizingStrategy("auto")
    
    def size(self):
        return self.nLines
    
    def addToLayout(self, name="", optionalCheckbox=None, nameLabel=None, valueField=None, tailWidget=None):
        grid = self.gridLayout
        rowIndex = self.size()
        items = [optionalCheckbox, nameLabel, valueField, tailWidget]
        self.applySizingStrategy(optionalCheckbox, nameLabel, valueField, tailWidget)

        if name not in self.sameRowSet:
            self.columnIndex = 0
        else:
            rowIndex -= 1
        
        for rank, item in enumerate(items):
            if item is not None:
                grid.addWidget(item, rowIndex, self.columnIndex + rank)
                item.setParent(self.getParentWidget())
            else:
                grid.addWidget(QLabel(f""), rowIndex, self.columnIndex + rank)

        self.columnIndex += len(items)
        if name not in self.sameRowSet:
            self.nLines += 1