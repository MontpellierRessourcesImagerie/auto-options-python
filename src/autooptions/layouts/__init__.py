from autooptions.layouts.grid_layout import GridLayout
from autooptions.layouts.vertical_layout import VerticalLayout


class LayoutFactory(object):

    availableLayouts = {"grid": GridLayout, "vertical": VerticalLayout}

    defaultLayout = GridLayout

    def get(self, layout_type):
        return self.availableLayouts.get(layout_type, self.defaultLayout)

    @staticmethod
    def createLayout(layout_type, same_row_set=None, parent=None):
        if type(layout_type) is str:
            layout_name = layout_type.lower()
            layout_args = {}
        elif type(layout_type) is dict:
            layout_name = layout_type.get("name", "vertical").lower()
            layout_args = {k: v for k, v in layout_type.items() if k != "name"}
        else:
            raise ValueError(f"Invalid layout_type: {layout_type}")
        layoutConstructor = LayoutFactory.availableLayouts.get(
            layout_name, LayoutFactory.defaultLayout
        )
        return layoutConstructor(
            same_row_set=same_row_set, parent=parent, **layout_args
        )
