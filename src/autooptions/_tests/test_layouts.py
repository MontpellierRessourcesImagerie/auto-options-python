import pytest
import os
import numpy as np

from autooptions.widget import OptionsWidget
from autooptions.options import Options
from autooptions.layouts import LayoutFactory


class TestLayoutUtils:

    @staticmethod
    def getLayoutsList():
        return list(LayoutFactory.availableLayouts.keys())


class TestLayouts:

    def onSomethingHappened(self, value):
        self.lastValue = value

    @pytest.fixture()
    def options(self):
        options = Options("Autooptions Test", "Layouts Test")
        options.addImage("image", value=None, transient=True, optional=(True, False))
        options.addLabels("labels", value="labels_layer", transient=True)
        options.addPoints("points", value="points_layer", transient=True)
        options.addFFT("fft", value=None, transient=True)
        options.addStr("group", value="lps", optional=(True, True))
        options.addInt("size xy", value=3)
        options.addInt("size z", value=1)
        options.addChoice(
            "footprint",
            choices=["none", "cube", "ball", "octahedron"],
            callback=self.onSomethingHappened,
        )
        options.addFloat("sigma", value=1.34)
        options.addBool("do it", value=True)
        yield options

    @pytest.mark.parametrize("layout_type", TestLayoutUtils.getLayoutsList())
    def testLayoutInstanciation(self, options, make_napari_viewer_proxy, layout_type):
        viewer = make_napari_viewer_proxy()
        widget = OptionsWidget(viewer, options, layout_type=layout_type, client=self)
        assert widget.options is options
        assert widget.viewer is viewer
        assert widget.client is self
        assert type(widget.layout()) is LayoutFactory.availableLayouts[layout_type]

    @pytest.mark.parametrize("layout_type", TestLayoutUtils.getLayoutsList())
    @pytest.mark.parametrize("same_row", [None, [], ["labels", "points"], ["size z"]])
    def testLayoutLength(
        self, options, make_napari_viewer_proxy, layout_type, same_row
    ):
        viewer = make_napari_viewer_proxy()
        widget = OptionsWidget(
            viewer, options, layout_type=layout_type, sameRowSet=same_row, client=self
        )
        n_widgets = len(options)
        expected = n_widgets - (len(same_row) if same_row else 0)
        assert widget.layout().size() == expected

    @pytest.mark.parametrize("field_width", [50, 300])
    def testLayoutSizingFixed(self, options, make_napari_viewer_proxy, field_width):
        viewer = make_napari_viewer_proxy()
        args = {"name": "vertical", "max_width": field_width}
        widget = OptionsWidget(viewer, options, layout_type=args, client=self)
        for _, w in widget.widgets.values():
            assert w.maximumWidth() == field_width

    @pytest.mark.parametrize("layout_type", TestLayoutUtils.getLayoutsList())
    def testWidgetsHierarchy(self, options, make_napari_viewer_proxy, layout_type):
        viewer = make_napari_viewer_proxy()
        widget = OptionsWidget(viewer, options, layout_type=layout_type, client=self)
        for cb, w in widget.widgets.values():
            assert w.parent() is widget
            assert w in widget.children()
            if cb is not None:
                assert cb.parent() is widget
                assert cb in widget.children()
