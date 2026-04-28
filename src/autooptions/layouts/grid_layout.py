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
    
    def size(self):
        return self.gridLayout.count()
    
    def addToLayout(self, name="", optionalCheckbox=None, nameLabel=None, valueField=None, tailWidget=None):
        grid = self.gridLayout
        rowIndex = self.size()
        items = [optionalCheckbox, nameLabel, valueField, tailWidget]
        
        for rank, item in enumerate(items):
            if item is not None:
                grid.addWidget(item, rowIndex, rank)
                item.setParent(self.getParentWidget())
            else:
                grid.addWidget(QLabel(f""), rowIndex, rank)