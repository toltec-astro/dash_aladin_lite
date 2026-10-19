# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.types import NumberType  # noqa: F401
except ImportError:
    # Backwards compatibility for dash<=4.1.0
    if typing.TYPE_CHECKING:
        raise
    NumberType = typing.Union[  # noqa: F401
        typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
    ]

ComponentSingleType = typing.Union[str, int, float, Component, None]
ComponentType = typing.Union[
    ComponentSingleType,
    typing.Sequence[ComponentSingleType],
]


class AladinLite(Component):
    """An AladinLite component.
Aladin Lite sky atlas with layers given as data and selection shared with
Dash.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    CSS class of the viewer element.

- fov (number; optional):
    Field of view, in degrees.

- layers (list of boolean | number | string | dict | lists; optional):
    Layers drawn over the survey. Each layer has a unique \"id\" and a
    \"type\": \"image\" (a FITS image by URL, over the survey or
    replacing it as the base image), \"catalog\" (sources with ids),
    or \"graphic\" (polylines, polygons and circles). A changed layer
    is redrawn on top; unchanged layers are kept. See
    dash_aladin_lite.layers.

- options (boolean | number | string | dict | list; optional):
    Aladin Lite options used when the viewer is created, e.g.
    {\"showCooGridControl\": True}. Later changes have no effect.

- selected_ids (list of string | numbers; optional):
    Ids of the selected entities. A click sets the ids of the objects
    under the cursor (none on empty sky), a region selection those
    inside it. Setting it highlights every source and shape with those
    ids.

- setProps (optional):
    Dash-assigned callback that reports property changes to Dash.

- survey (string; optional):
    Base HiPS survey, by ID or URL, e.g. \"P/DSS2/color\".

- target (string; optional):
    View center: an object name (resolved by Sesame) or \"ra dec\" in
    degrees."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_aladin_lite'
    _type = 'AladinLite'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[typing.Union[str]] = None,
        style: typing.Optional[typing.Any] = None,
        target: typing.Optional[typing.Union[str]] = None,
        fov: typing.Optional[typing.Union[NumberType]] = None,
        survey: typing.Optional[typing.Union[str]] = None,
        options: typing.Optional[typing.Any] = None,
        layers: typing.Optional[typing.Union[typing.Sequence[typing.Any]]] = None,
        selected_ids: typing.Optional[typing.Union[typing.Sequence[typing.Union[str, NumberType]]]] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'className', 'fov', 'layers', 'options', 'selected_ids', 'setProps', 'style', 'survey', 'target']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'fov', 'layers', 'options', 'selected_ids', 'setProps', 'style', 'survey', 'target']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AladinLite, self).__init__(**args)

setattr(AladinLite, "__init__", _explicitize_args(AladinLite.__init__))
