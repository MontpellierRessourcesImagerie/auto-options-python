from abc import abstractmethod
from qtpy.QtWidgets import (
    QVBoxLayout,
    QSizePolicy
)

class BaseLayout(QVBoxLayout):
    def __init__(self, parent=None, same_row_set=None):
        super().__init__()
        self.parent = parent
        self.sameRowSet = set() if same_row_set is None else same_row_set.copy()
        self.sizingStrategy = None
        self.fieldWith = 50

    def setSizingStrategy(self, strategy, fieldWith=None):
        self.sizingStrategy = strategy
        if fieldWith is not None:
            self.fieldWith = fieldWith

    def getParentWidget(self):
        return self.parent

    @abstractmethod
    def size(self):
        raise NotImplementedError("size method must be implemented by subclasses")

    @abstractmethod
    def addToLayout(self, name="", optionalCheckbox=None, nameLabel=None, valueField=None, tailWidget=None):
        raise NotImplementedError("addToLayout method must be implemented by subclasses")
    
    def applySizingStrategy(self, optionalCheckbox=None, nameLabel=None, valueField=None, tailWidget=None):
        if self.sizingStrategy == "fixed":
            self.applyFixedSizingStrategy(optionalCheckbox, nameLabel, valueField, tailWidget)
        elif self.sizingStrategy == "auto":
            self.applyAutoSizingStrategy(optionalCheckbox, nameLabel, valueField, tailWidget)
        else:
            raise ValueError(f"Unknown sizing strategy: {self.sizingStrategy}")
    
    def applyFixedSizingStrategy(self, optionalCheckbox=None, nameLabel=None, valueField=None, tailWidget=None):
        if optionalCheckbox is not None:
            height = optionalCheckbox.sizeHint().height()
            optionalCheckbox.setFixedWidth(height + 5)
        if valueField is not None:
            valueField.setMaximumWidth(self.fieldWith)
        if tailWidget is not None:
            height = tailWidget.sizeHint().height()
            tailWidget.setFixedWidth(height + 5)

    def applyAutoSizingStrategy(self, optionalCheckbox=None, nameLabel=None, valueField=None, tailWidget=None):
        if optionalCheckbox is not None:
            optionalCheckbox.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        if nameLabel is not None:
            nameLabel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        if valueField is not None:
            valueField.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        if tailWidget is not None:
            tailWidget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)