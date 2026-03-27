from napari.layers.labels.labels import Labels
from napari.layers.points.points import Points
from napari.layers.image.image import Image



class NapariUtil:
    """ Utility methods for the napari image viewer.
    """

    def __init__(self, viewer):
        """ Constructor.

        :param viewer: the napari viewer
        :type viewer: napari.viewer.Viewer
        """
        self.viewer = viewer


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
        fftLayers = [layer.name for layer in imageLayers if 'fft' in layer.metadata.keys()]
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
        """ Answer the layer with the given name, if it exists and None otherwise.

        :param name: The name of a layer
        :return: The layer from napari's layer list that has the given name
        """
        for layer in self.viewer.layers:
            if layer.name == name:
                return layer
        return None


    def getDataAndScaleOfLayerWithName(self, name):
        """ Answer the data, the scale and the unit of the layer with the given name.

        :param name: The name of a layer
        :return: A tupel with the data, the scale and the unit of the layer with the given name.
                 The unit is the unit of the first dimension. The unit is supposed to be the same for all dimensions.
        """
        layer = self.getLayerWithName(name)
        return layer.data, layer.scale, str(layer.units[0])


    @staticmethod
    def getOriginalPath(layer):
        """ Answer the source path of the layer if it represents an image opened from the filesystem and the
        original path from the metadata if it is a derived image. If it is neither an image opened from a file nor
        derived from one (for example an image programmatically created) answer None. For the metadata information to
        be present, the image operations must set it.

        :param layer: The input layer
        :return: The path of the image in the filesystem if it is known
        """
        if 'original_path' in layer.metadata.keys():
            return layer.metadata['original_path']
        if layer.source.path:
            return layer.source.path
        return None


    @staticmethod
    def copyOriginalPath(srcLayer, destLayer):
        """Copy the orignal path from one layer to another. This should be used by operations that create images derived
        from an input image.

        :param srcLayer: The layer from which the original path is copied.
        :param destLayer: The layer to which the original path is copied.
        """
        path = NapariUtil.getOriginalPath(srcLayer)
        destLayer.metadata['original_path'] = path

