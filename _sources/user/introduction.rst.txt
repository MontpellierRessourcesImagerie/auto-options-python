Introduction
============
.. figure:: https://dev.mri.cnrs.fr/attachments/download/4544/autooptions_conv.png
    :width: 250
    :align: center
    :alt: the napari-bigfish plugin

    Fig. 1.1 - A simple dialog created with autooptions

Autooptions allows to create options for operations in napari, in a simple way. Autooptions automatically saves and
loads non transient options. It can create a dialog from the options, in which the user can change the values of the
options. It updates combo-boxes containing layers of a given type when layers of that type are added or removed in
napari. The user can provide callbacks that are called when the value of an option changes.

The option types currently supported are:

- Image
- FFT (specific to 3D-toolbox)
- Labels
- Points
- Int
- Float
- Choice
- String
- Boolean

The layer types (FFT, Labels, Points and Image) and Choice will be represented via combo-boxes in the dialog. Boolean
is using a checkbox and the others are using input fields.

The code to create the options-dialog in Fig.1.1 is:

.. code-block:: python

   import napari
   from autooptions.options import Options
   from autooptions.widget import OptionsWidget

   viewer = napari.Viewer()
   options = Options("3D Toolbox", "Convolution")
   options.addImage()
   options.addImage(name="kernel")
   options.addChoice("mode", choices=["same", "valid", "full"])
   options.addChoice("method", choices=["auto", "direct", "fft"])
   options.load()
   widget = OptionsWidget(viewer, options, viewer)
   widget.addApplyButton(None)
   viewer.window.add_dock_widget(widget, name=options.optionsName)
