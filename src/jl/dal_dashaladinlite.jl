# AUTO GENERATED FILE - DO NOT EDIT

export dal_dashaladinlite

"""
    dal_dashaladinlite(;kwargs...)

A DashAladinLite component.
DashAladinLite
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `autoFov` (Bool; optional): Adjust the fov automatically for target if set to True.
- `className` (String; optional): The class of the container.
- `custom_script_calls` (Dict; optional): Custom script calls to make. The keys should match those in
``custom_script``, and the vialues are passed to
``custom_scripts``.
- `custom_scripts` (Dict; optional): Custom scripts to be used in ``custom_script_calls``.
The values are inline functions that have signature like
``function(aladin, data, props)``, where data are
passed in ``custom_script_calls``.
- `footprintClicked` (Dict; optional): Clicked footprint.
- `footprintHovered` (Dict; optional): Hovered footprint.
- `fov` (Real; optional): The FOV of the display.
- `layers` (optional): Layers to show.
Each layer can be one of types ['catalog', 'overlay', 'moc'].. layers has the following type: Array of lists containing elements 'type', 'data', 'options'.
Those elements have the following types:
  - `type` (a value equal to: "catalog"; optional)
  - `data` (optional): . data has the following type: String | Array of lists containing elements 'ra', 'dec'.
Those elements have the following types:
  - `ra` (Real; optional)
  - `dec` (Real; optional)s
  - `options` (optional): . options has the following type: lists containing elements 'show', 'name', 'color', 'sourceSize', 'shape', 'maxNbsources', 'raField', 'decField', 'displayLabel', 'labelColor', 'labelFont', 'labelColumn', 'onClick'.
Those elements have the following types:
  - `show` (Bool; optional)
  - `name` (String; optional)
  - `color` (String; optional)
  - `sourceSize` (Real; optional)
  - `shape` (a value equal to: 'circle', "plus", "rhomb", 'cross', 'triangle', 'square'; optional)
  - `maxNbsources` (Real; optional)
  - `raField` (String; optional)
  - `decField` (String; optional)
  - `displayLabel` (Bool; optional)
  - `labelColor` (String; optional)
  - `labelFont` (String; optional)
  - `labelColumn` (String; optional)
  - `onClick` (a value equal to: 'showTable', 'showPopup'; optional) | lists containing elements 'type', 'data', 'options'.
Those elements have the following types:
  - `type` (a value equal to: "overlay"; optional)
  - `data` (optional): . data has the following type: Array of lists containing elements 'type', 'ra', 'dec', 'radius', 'color'.
Those elements have the following types:
  - `type` (a value equal to: 'circle'; optional)
  - `ra` (Real; optional)
  - `dec` (Real; optional)
  - `radius` (Real; optional)
  - `color` (String; optional) | lists containing elements 'type', 'data', 'color', 'lineWidth'.
Those elements have the following types:
  - `type` (a value equal to: 'polyline'; optional)
  - `data` (Array of Arrays; optional)
  - `color` (String; optional)
  - `lineWidth` (Real; optional) | lists containing elements 'type', 'data'.
Those elements have the following types:
  - `type` (a value equal to: 'polygon'; optional)
  - `data` (Array of Arrays; optional)s
  - `options` (optional): . options has the following type: lists containing elements 'show', 'name', 'color', 'lineWidth'.
Those elements have the following types:
  - `show` (Bool; optional)
  - `name` (String; optional)
  - `color` (String; optional)
  - `lineWidth` (Real; optional) | lists containing elements 'type', 'data', 'options'.
Those elements have the following types:
  - `type` (a value equal to: 'moc'; optional)
  - `data` (String | Dict; optional)
  - `options` (optional): . options has the following type: lists containing elements 'show', 'name', 'color', 'opacity', 'adaptativeDisplay'.
Those elements have the following types:
  - `show` (Bool; optional)
  - `name` (String; optional)
  - `color` (String; optional)
  - `opacity` (Real; optional)
  - `adaptativeDisplay` (Bool; optional)s
- `objectClicked` (Dict; optional): Clicked object.
- `objectHovered` (Dict; optional): Hovered object.
- `options` (Dict; optional): Additional options passed to the aladinlite.js
- `position` (Dict; optional): Position.
- `style` (Dict; optional): The style of the container.
- `survey` (optional): The survey to display as base image layer.. survey has the following type: String | lists containing elements 'id', 'name', 'rootUrl', 'cooFrame', 'maxOrder', 'options'.
Those elements have the following types:
  - `id` (String; optional)
  - `name` (String; optional)
  - `rootUrl` (String; optional)
  - `cooFrame` (a value equal to: 'equatorial', 'galactic'; optional)
  - `maxOrder` (Real; optional)
  - `options` (optional): . options has the following type: lists containing elements 'imgFormat'.
Those elements have the following types:
  - `imgFormat` (a value equal to: 'jpeg', 'fits', 'png'; optional)
- `target` (String; required): The target to display.
"""
function dal_dashaladinlite(; kwargs...)
        available_props = Symbol[:id, :autoFov, :className, :custom_script_calls, :custom_scripts, :footprintClicked, :footprintHovered, :fov, :layers, :objectClicked, :objectHovered, :options, :position, :style, :survey, :target]
        wild_props = Symbol[]
        return Component("dal_dashaladinlite", "DashAladinLite", "dash_aladin_lite", available_props, wild_props; kwargs...)
end

