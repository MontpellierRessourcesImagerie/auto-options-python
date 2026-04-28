from autooptions.layouts.grid_layout import GridLayout
from autooptions.layouts.vertical_layout import VerticalLayout

class LayoutFactory(object):
    
    availableLayouts = {
        'grid'    : GridLayout,
        'vertical': VerticalLayout
    }

    defaultLayout = GridLayout
    
    @staticmethod
    def createLayout(layout_type, parent=None):
        layoutConstructor = LayoutFactory.availableLayouts.get(
            layout_type, 
            LayoutFactory.defaultLayout
        )
        return layoutConstructor(parent)