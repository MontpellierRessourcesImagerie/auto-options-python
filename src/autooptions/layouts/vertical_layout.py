from qtpy.QtWidgets import (
    QHBoxLayout,
    QLabel
)

from autooptions.layouts.base_layout import BaseLayout

class VerticalLayout(BaseLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nRows = 0
        self.padSlots = False

    def setPadSlots(self, pad):
        self.padSlots = pad
    
    def size(self):
        return self.nRows
    
    def addToLayout(self, optionalCheckbox=None, nameLabel=None, valueField=None, tailWidget=None):
        widgets = [optionalCheckbox, nameLabel, valueField, tailWidget]
        h_layout = QHBoxLayout()
        for widget in widgets:
            if widget is not None:
                h_layout.addWidget(widget)
                widget.setParent(self.getParentWidget())
            elif self.padSlots:
                h_layout.addWidget(QLabel(f""))
        self.addLayout(h_layout)
        self.nRows += 1
