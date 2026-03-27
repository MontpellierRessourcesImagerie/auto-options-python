import pytest
import numpy as np
from napari.layers import Labels, Image, Points
from autooptions.napari_util import NapariUtil

class Layer:
    pass



@pytest.fixture
def layers():
    layers = []
    layers.append( Image(np.zeros(shape=(3, 3), dtype=np.uint8), name="toad", metadata={'fft': 'fft'}) )
    layers.append( Image(np.zeros(shape=(3, 3), dtype=np.uint8), name="frog", scale=(1,3), units="nm") )
    layers.append( Points(np.zeros((3, 3)), name="ant") )
    layers.append( Labels(np.zeros(shape=(4, 4), dtype=np.uint8), name="oak") )
    layers.append( Points(np.zeros((2, 3)), name="bee") )
    layers.append( Image(np.zeros(shape=(3, 3), dtype=np.uint8), name="bird") )
    yield layers



def test_constructor(make_napari_viewer_proxy):
    viewer = make_napari_viewer_proxy()
    napariUtil = NapariUtil(viewer)
    assert napariUtil.viewer == viewer


def testGetImageLayers(make_napari_viewer_proxy, layers):
    viewer = make_napari_viewer_proxy()
    napariUtil = NapariUtil(viewer)
    for layer in layers:
        viewer.add_layer(layer)

    assert len(napariUtil.getImageLayers()) == 3
    assert napariUtil.getImageLayers()[0] == "toad"
    assert napariUtil.getImageLayers()[1] == "frog"
    assert napariUtil.getImageLayers()[2] == "bird"


def testGetFFTLayers(make_napari_viewer_proxy, layers):
    viewer = make_napari_viewer_proxy()
    napariUtil = NapariUtil(viewer)
    for layer in layers:
        viewer.add_layer(layer)

    fftLayers = napariUtil.getFFTLayers()
    assert len(fftLayers) == 1
    assert fftLayers[0] == 'toad'


def testGetLabelLayers(make_napari_viewer_proxy, layers):
    viewer = make_napari_viewer_proxy()
    napariUtil = NapariUtil(viewer)
    for layer in layers:
        viewer.add_layer(layer)

    labelLayers = napariUtil.getLabelLayers()
    assert len(labelLayers) == 1
    assert 'oak' == labelLayers[0]


def testGetPointLayers(make_napari_viewer_proxy, layers):
    viewer = make_napari_viewer_proxy()
    napariUtil = NapariUtil(viewer)
    for layer in layers:
        viewer.add_layer(layer)

    pointLayers = napariUtil.getPointsLayers()
    assert len(pointLayers) == 2
    assert pointLayers[0] == 'ant'
    assert pointLayers[1] == 'bee'


def testGetLayersOfType(make_napari_viewer_proxy, layers):
    viewer = make_napari_viewer_proxy()
    napariUtil = NapariUtil(viewer)
    for layer in layers:
        viewer.add_layer(layer)

    labelLayers = napariUtil.getLayersOfType(Labels)
    assert len(labelLayers) == 1
    assert labelLayers[0] == 'oak'


def testGetDataOfLayerWithName(make_napari_viewer_proxy, layers):
    viewer = make_napari_viewer_proxy()
    napariUtil = NapariUtil(viewer)
    for layer in layers:
        viewer.add_layer(layer)

    data = napariUtil.getDataOfLayerWithName("oak")
    assert data.shape == (4,4)
    data = napariUtil.getDataOfLayerWithName("marsupilami")
    assert data is None


def testGetLayerWithName(make_napari_viewer_proxy, layers):
    viewer = make_napari_viewer_proxy()
    napariUtil = NapariUtil(viewer)
    for layer in layers:
        viewer.add_layer(layer)

    layer = napariUtil.getLayerWithName("bee")
    assert layer.name == "bee"
    layer = napariUtil.getLayerWithName("marsupilami")
    assert layer is None


def testGetDataAndScaleOfLayerWithName(make_napari_viewer_proxy, layers):
    viewer = make_napari_viewer_proxy()
    napariUtil = NapariUtil(viewer)
    for layer in layers:
        viewer.add_layer(layer)

    data, scale, unit = napariUtil.getDataAndScaleOfLayerWithName('frog')
    assert data.shape == (3,3)
    assert scale[0] == 1
    assert scale[1] == 3
    assert unit == "nanometer"


def testGetOriginalPath(make_napari_viewer_proxy, layers):
    viewer = make_napari_viewer_proxy()
    napariUtil = NapariUtil(viewer)
    for layer in layers:
        viewer.add_layer(layer)
    toad = napariUtil.getLayerWithName('toad')
    toad.metadata['original_path'] = "d/e/f"
    assert napariUtil.getOriginalPath(napariUtil.getLayerWithName('bee')) is None
    layer = Layer()
    layer.source = Layer()
    layer.source.path = "a/b/c"
    layer.metadata = {}
    assert napariUtil.getOriginalPath(layer)
    assert napariUtil.getOriginalPath(toad) == 'd/e/f'


def testCopOriginalPath(make_napari_viewer_proxy, layers):
    viewer = make_napari_viewer_proxy()
    napariUtil = NapariUtil(viewer)
    for layer in layers:
        viewer.add_layer(layer)
    toad = napariUtil.getLayerWithName('toad')
    toad.metadata['original_path'] = "d/e/f"
    frog = napariUtil.getLayerWithName('frog')
    napariUtil.copyOriginalPath(toad, frog)
    assert napariUtil.getOriginalPath(frog) == "d/e/f"
