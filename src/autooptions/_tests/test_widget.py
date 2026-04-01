import pytest
import os
import numpy as np
from autooptions.widget import OptionsWidget
from autooptions.options import Options

class FakeEvent:
    modifiers = {}


class TestOptionsWidget:



    def onSomethingHappened(self, value):
        self.lastValue = value


    @pytest.fixture()
    def options(self):
        options = Options("Autooptions Test", "Widget Test")
        options.addImage('image', value=None, transient=True)
        options.addLabels('labels', value='labels_layer', transient=True)
        options.addPoints('points', value='points_layer', transient=True)
        options.addFFT('fft', value=None, transient=True)
        options.addStr("group", value="lps")
        options.addInt('size xy', value=3)
        options.addInt('size z', value=1)
        options.addChoice('footprint', choices=["none", "cube", "ball", "octahedron"], callback=self.onSomethingHappened)
        options.addFloat('sigma', value=1.34)
        options.addBool('do it', value=True)
        yield options


    def testConstructor(self, options, make_napari_viewer_proxy):
        viewer = make_napari_viewer_proxy()
        widget = OptionsWidget(viewer, options, self)
        assert widget.options is options
        assert widget.viewer is viewer
        assert widget.client is self


    def testAddApplyButton(self, options, make_napari_viewer_proxy, mocker):
        viewer = make_napari_viewer_proxy()
        widget = OptionsWidget(viewer, options, self)
        assert widget.getApplyButton() is None
        callback = mocker.stub(name='onApplyButtonPressed')
        widget.addApplyButton(callback)
        assert not widget.getApplyButton() is None
        assert callback.call_count == 0


    def testAddOKButton(self, options, make_napari_viewer_proxy, mocker):
        viewer = make_napari_viewer_proxy()
        widget = OptionsWidget(viewer, options, self)
        assert widget.getOKButton() is None
        callback = mocker.stub(name='onOKButtonPressed')
        widget.addOKButton(callback)
        assert not widget.getOKButton() is None
        assert callback.call_count == 0


    def testAddCancelButton(self, options, make_napari_viewer_proxy, mocker):
        viewer = make_napari_viewer_proxy()
        widget = OptionsWidget(viewer, options, self)
        assert widget.getCancelButton() is None
        callback = mocker.stub(name='onCancelButtonPressed')
        widget.addCancelButton(callback)
        assert not widget.getCancelButton() is None
        assert callback.call_count == 0


    def test_OnApplyButtonClicked(self, options, make_napari_viewer_proxy, mocker):
        viewer = make_napari_viewer_proxy()
        widget = OptionsWidget(viewer, options, self)
        callback = mocker.stub(name='self.apply')
        widget.addApplyButton(callback)
        options.setValue('group', 'xps')
        if os.path.exists(options.optionsPath):
            os.remove(options.optionsPath)
        widget._onApplyButtonClicked()
        assert os.path.exists(options.optionsPath)
        assert options.value("group") == "lps"


    def test_OnOKButtonClicked(self, options, make_napari_viewer_proxy, mocker):
        viewer = make_napari_viewer_proxy()
        widget = OptionsWidget(viewer, options, self)
        callback = mocker.stub(name='self.ok')
        widget.addOKButton(callback)
        viewer.window.add_dock_widget(widget, name=options.optionsName)
        options.setValue('group', 'xps')
        if os.path.exists(options.optionsPath):
            os.remove(options.optionsPath)
        widget._onOKButtonClicked()
        assert os.path.exists(options.optionsPath)
        assert options.value("group") == "lps"


    def test_OnCancelButtonClicked(self, options, make_napari_viewer_proxy, mocker):
        viewer = make_napari_viewer_proxy()
        widget = OptionsWidget(viewer, options, self)
        callback = mocker.stub(name='self.cancel')
        widget.addCancelButton(callback)
        viewer.window.add_dock_widget(widget, name=options.optionsName)
        options.setValue('group', 'xps')
        if os.path.exists(options.optionsPath):
            os.remove(options.optionsPath)
        widget._onCancelButtonClicked()
        assert not os.path.exists(options.optionsPath)
        assert options.value("group") == "xps"


    def test_OnLayerAddedOrRemoved(self, options, make_napari_viewer_proxy):
        viewer = make_napari_viewer_proxy()
        widget = OptionsWidget(viewer, options, self)
        viewer.window.add_dock_widget(widget, name=options.optionsName)
        data = np.random.rand(12, 12)
        viewer.add_image(data=data, name='data')
        assert True


    def testGetImageLayer(self, options, make_napari_viewer_proxy):
        viewer = make_napari_viewer_proxy()
        widget = OptionsWidget(viewer, options, self)
        viewer.window.add_dock_widget(widget, name=options.optionsName)
        data = np.random.rand(12, 12)
        viewer.add_image(data=data, name='labels_layer')
        layer = widget.getImageLayer("labels")
        assert layer is not None
        assert layer.name == "labels_layer"
        assert layer.data.shape == (12, 12)