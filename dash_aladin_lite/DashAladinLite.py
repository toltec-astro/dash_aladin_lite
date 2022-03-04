# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashAladinLite(Component):
    """A DashAladinLite component.
DashAladinLite

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- autoFov (boolean; default False):
    Adjust the fov automatically for target if set to True.

- className (string; optional):
    The class of the container.

- footprintClicked (dict; optional):
    Clicked footprint.

- footprintHovered (dict; optional):
    Hovered footprint.

- fov (number; default 10):
    The FOV of the display.

- layers (list of dicts; optional):
    Layers to show. Each layer can be one of types ['catalog',
    'overlay', 'moc'].

    `layers` is a list of dicts with keys:

    - data (dict; optional)

        `data` is a string

      Or list of dicts with keys:

        - dec (number; optional)

        - ra (number; optional)

    - options (dict; optional)

        `options` is a dict with keys:

        - color (string; optional)

        - decField (string; optional)

        - displayLabel (boolean; optional)

        - labelColor (string; optional)

        - labelColumn (string; optional)

        - labelFont (string; optional)

        - maxNbsources (number; optional)

        - name (string; optional)

        - onClick (a value equal to: 'showTable', 'showPopup'; optional)

        - raField (string; optional)

        - shape (a value equal to: 'circle', "plus", "rhomb", 'cross', 'triangle', 'square'; optional)

        - show (boolean; optional)

        - sourceSize (number; optional)

    - type (a value equal to: "catalog"; optional) | dict with keys:

    - data (list of dicts; optional)

        `data` is a list of dicts with keys:

        - color (string; optional)

        - dec (number; optional)

        - ra (number; optional)

        - radius (number; optional)

        - type (a value equal to: 'circle'; optional)

              Or dict with keys:

        - color (string; optional)

        - data (list of lists; optional)

        - lineWidth (number; optional)

        - type (a value equal to: 'polyline'; optional) | dict with keys:

        - data (list of lists; optional)

        - type (a value equal to: 'polygon'; optional)

    - options (dict; optional)

        `options` is a dict with keys:

        - color (string; optional)

        - lineWidth (number; optional)

        - name (string; optional)

        - show (boolean; optional)

    - type (a value equal to: "overlay"; optional) | dict with keys:

    - data (string | dict; optional)

    - options (dict; optional)

        `options` is a dict with keys:

        - adaptativeDisplay (boolean; optional)

        - color (string; optional)

        - name (string; optional)

        - opacity (number; optional)

        - show (boolean; optional)

    - type (a value equal to: 'moc'; optional)

- objectClicked (dict; optional):
    Clicked object.

- objectHovered (dict; optional):
    Hovered object.

- options (dict; default {    "showFullscreenControl": False,}):
    Additional options passed to the aladinlite.js.

- position (dict; optional):
    Position.

- style (dict; optional):
    The style of the container.

- survey (dict; default 'P/DSS2/color'):
    The survey to display as base image layer.

    `survey` is a string | dict with keys:

    - cooFrame (a value equal to: 'equatorial', 'galactic'; optional)

    - id (string; optional)

    - maxOrder (number; optional)

    - name (string; optional)

    - options (dict; optional)

        `options` is a dict with keys:

        - imgFormat (a value equal to: 'jpeg', 'fits', 'png'; optional)

    - rootUrl (string; optional)

- target (string; required):
    The target to display."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, target=Component.REQUIRED, fov=Component.UNDEFINED, autoFov=Component.UNDEFINED, survey=Component.UNDEFINED, layers=Component.UNDEFINED, options=Component.UNDEFINED, objectClicked=Component.UNDEFINED, objectHovered=Component.UNDEFINED, footprintClicked=Component.UNDEFINED, footprintHovered=Component.UNDEFINED, position=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'autoFov', 'className', 'footprintClicked', 'footprintHovered', 'fov', 'layers', 'objectClicked', 'objectHovered', 'options', 'position', 'style', 'survey', 'target']
        self._type = 'DashAladinLite'
        self._namespace = 'dash_aladin_lite'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'autoFov', 'className', 'footprintClicked', 'footprintHovered', 'fov', 'layers', 'objectClicked', 'objectHovered', 'options', 'position', 'style', 'survey', 'target']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['target']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashAladinLite, self).__init__(**args)
