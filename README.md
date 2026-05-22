# auto-options-python

Mange command options in python and create QWidgets for them.

## Introduction

<figure>
  <img src="https://github.com/user-attachments/assets/ea23f8a5-81d7-4524-90d0-9d5a4daaea63" alt="A simple options dialog" style="width:250", align='center'>
  <figcaption>Fig. 1.1 - A simple dialog created with autooptions</figcaption>
</figure>

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

```python
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
 widget = OptionsWidget(viewer, options, layout_type="vertical")
 widget.addApplyButton(None)
 viewer.window.add_dock_widget(widget, name=options.optionsName)
```

You can access the user input of the widgets via the options name:

```python
    print(options.value("image"))
    print(options.value("method"))
```
The shortcut ``getImageLayer``, allows to directly retrieve the layer selected in the widget, without retrieving the name first and then the layer.

```python
kernelLayer = widget.getImageLayer("kernel")
```

You can register callbacks for options and for buttons. The callback of an option is called when the user input for the option changed. For the predifined buttons ``apply`` and ``ok`` the values are automatically copied from the widget into the option, before the user registered callback is called.

```python
 options = Options("3D Toolbox", "Convolution")
 options.addImage(callback, callback=self.onInputImageChanged)
 self.widget = OptionsWidget(self.viewer, self.options, client=self)
 widget.addApplyButton(self.handleApplyButtonPressed)
```

You can access a widget, for example to check that only valid values can be entered:

```python
    def onInputChanged(self, value):
        if not value.isnumeric():
            self.widget.widgets["size xy"][1].setText(str(self.options.value("size xy")))
```

You can create optional options :) These are displayed with a checkbox to activate/deactivate them. When deactivated the option will be ignored. This allows to avoid the usage of special values in options that indicate for example that the user doesn't want to enter a value for the option in which case a default or on the fly calculated value is used. 

```python
options = Options("Filament Toolbox", "measure_labels")
options.addLabels()
options.addImage(optional=[True, False])
```
``[True, False]`` indicates that the option is optional and by default deactivated. The value of a deactivated option will be ``None``. 

<figure>
  <img src="https://github.com/user-attachments/assets/cd4cdbf3-a626-4c37-b1b5-76481c21cf61" alt="An optional option" style="width:250", align='center'>
  <figcaption>Fig. 1.2 - The image option is optional</figcaption>
</figure>

