from napari.layers.labels.labels import Labels
from napari.layers.points.points import Points
from napari.layers.image.image import Image
from napari.layers.shapes.shapes import Shapes



class NapariUtil:
    """ Utility methods for the napari image viewer.
    """

    def __init__(self, viewer):
        """ Constructor.

        :param viewer: the napari viewer
        :type viewer: napari.viewer.Viewer
        """
        self.viewer = viewer

    
    def getCurrentLayerOfType(self, layerType):
        """ Return the currently selected layer if it is of type layerType

        :param layerType: A napari layer type like Labels or Points.
        :return: The current layer if it is of the given type and None otherwise
        """
        layer = self.viewer.layers.selection.active
        return layer if isinstance(layer, layerType) else None
    

    def getCurrentImageLayer(self):
        """ Return the currently selected image layer

        :return: The current image layer if it exists and None otherwise
        :rtype: napari.layers.image.Image.Image
        """
        return self.getCurrentLayerOfType(Image)
    

    def getCurrentLabelsLayer(self):
        """ Return the currently selected label layer

        :return: The current label layer if it exists and None otherwise
        :rtype: napari.layers.labels.labels.Labels
        """
        return self.getCurrentLayerOfType(Labels)
    

    def getCurrentPointsLayer(self):
        """ Return the currently selected points layer

        :return: The current points layer if it exists and None otherwise
        :rtype: napari.layers.points.points.Points
        """
        return self.getCurrentLayerOfType(Points)
    

    def getCurrentShapesLayer(self):
        """ Return the currently selected shapes layer

        :return: The current shapes layer if it exists and None otherwise
        :rtype: napari.layers.shapes.shapes.Shapes
        """
        return self.getCurrentLayerOfType(Shapes)


    def getImageLayers(self):
        """ Return all image layers

                :return: A list of the image layers in the viewer
                :rtype: [napari.layers.image.Image.Image]
                """
        return self.getLayersOfType(Image)


    def getFFTLayers(self):
        """ Return all fft layers

                        :return: A list of the fft layers in the viewer
                        :rtype: [napari.layers.image.Image.Image]
                        """
        imageLayers = self.getImageLayers()
        imageLayers = [self.getLayerWithName(name) for name in imageLayers]
        fftLayers = [layer.name for layer in imageLayers if (layer is not None) and ('fft' in layer.metadata.keys())]
        return fftLayers


    def getLabelLayers(self):
        """ Return all label layers

        :return: A list of the label layers in the viewer
        :rtype: [napari.layers.labels.labels.Labels]
        """
        return self.getLayersOfType(Labels)


    def getPointsLayers(self):
        """ Return all point layers

        :return: A list of the point layers in the viewer
        :rtype: [napari.layers.points.points.Points]
        """
        return self.getLayersOfType(Points)
    

    def getShapesLayers(self):
        """ Return all shapes layers

        :return: A list of the shapes layers in the viewer
        :rtype: [napari.layers.shapes.shapes.Shapes]
        """
        return self.getLayersOfType(Shapes)


    def getLayersOfType(self, layerType):
        """ Return all layers of type layerType in the viewer

        :param layerType: A napari layer type like Labels or Points.
        :return: A list of the layers with the given type
        """
        layers = [layer.name for layer in self.viewer.layers if isinstance(layer, layerType)]
        return layers


    def getDataOfLayerWithName(self, name):
        """ Return the data of the layer with the given name.

        :param name: The name of the layer
        :type name: str
        :return: The layer with the given name if it exists and None otherwise
        """
        layer = self.getLayerWithName(name)
        if layer:
            return layer.data
        else:
            return None


    def getLayerWithName(self, name):
        for layer in self.viewer.layers:
            if layer.name == name:
                return layer
        return None


    def getDataAndScaleOfLayerWithName(self, name):
        layer = self.getLayerWithName(name)
        return (layer.data, layer.scale, str(layer.units[0])) if layer else (None, None, None)


    @staticmethod
    def getOriginalPath(layer):
        if 'original_path' in layer.metadata.keys():
            return layer.metadata['original_path']
        if layer.source.path:
            return layer.source.path
        return None


    @staticmethod
    def copyOriginalPath(srcLayer, destLayer):
        path = NapariUtil.getOriginalPath(srcLayer)
        destLayer.metadata['original_path'] = path

