from abc import abstractmethod
from qtpy.QtWidgets import QVBoxLayout

class BaseLayout(QVBoxLayout):
    def __init__(self, parent=None, same_row_set=None):
        super().__init__()
        self.parent = parent
        self.sameRowSet = set() if same_row_set is None else same_row_set.copy()

    def getParentWidget(self):
        return self.parent

    @abstractmethod
    def size(self):
        raise NotImplementedError("size method must be implemented by subclasses")

    @abstractmethod
    def addToLayout(self, name="", optionalCheckbox=None, nameLabel=None, valueField=None, tailWidget=None):
        raise NotImplementedError("addToLayout method must be implemented by subclasses")