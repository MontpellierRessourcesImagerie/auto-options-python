from qtpy.QtWidgets import (
    QHBoxLayout,
    QLabel
)

from autooptions.layouts.base_layout import BaseLayout

class VerticalLayout(BaseLayout):
    def __init__(self, same_row_set=None, parent=None):
        super().__init__(parent, same_row_set)
        self.nRows = 0
        self.padSlots = False
        self.lastLayout = None
        self.setSizingStrategy("fixed", 150)

    def setPadSlots(self, pad):
        self.padSlots = pad
    
    def size(self):
        return self.nRows
    
    def addToLayout(self, name="", optionalCheckbox=None, nameLabel=None, valueField=None, tailWidget=None):
        widgets = [optionalCheckbox, nameLabel, valueField, tailWidget]
        self.applySizingStrategy(optionalCheckbox, nameLabel, valueField, tailWidget)

        h_layout = QHBoxLayout() if name not in self.sameRowSet else self.lastLayout
        container = QHBoxLayout()

        for widget in widgets:
            if widget is not None:
                container.addWidget(widget)
                widget.setParent(self.getParentWidget())
            elif self.padSlots:
                container.addWidget(QLabel(f""))
        
        h_layout.addLayout(container)
        if name not in self.sameRowSet:
            self.addLayout(h_layout)
            self.nRows += 1
        self.lastLayout = h_layout
        