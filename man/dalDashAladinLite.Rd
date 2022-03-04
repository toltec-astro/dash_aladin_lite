% Auto-generated: do not edit by hand
\name{dalDashAladinLite}

\alias{dalDashAladinLite}

\title{DashAladinLite component}

\description{
DashAladinLite
}

\usage{
dalDashAladinLite(id=NULL, autoFov=NULL, className=NULL,
footprintClicked=NULL, footprintHovered=NULL, fov=NULL,
layers=NULL, objectClicked=NULL, objectHovered=NULL,
options=NULL, position=NULL, style=NULL, survey=NULL,
target=NULL)
}

\arguments{
\item{id}{Character. The ID used to identify this component in Dash callbacks.}

\item{autoFov}{Logical. Adjust the fov automatically for target if set to True.}

\item{className}{Character. The class of the container.}

\item{footprintClicked}{Named list. Clicked footprint.}

\item{footprintHovered}{Named list. Hovered footprint.}

\item{fov}{Numeric. The FOV of the display.}

\item{layers}{List of lists containing elements 'type', 'data', 'options'.
those elements have the following types:
  - type (a value equal to: "catalog"; optional)
  - data (optional): . data has the following type: character | list of lists containing elements 'ra', 'dec'.
those elements have the following types:
  - ra (numeric; optional)
  - dec (numeric; optional)s
  - options (optional): . options has the following type: lists containing elements 'show', 'name', 'color', 'sourcesize', 'shape', 'maxnbsources', 'rafield', 'decfield', 'displaylabel', 'labelcolor', 'labelfont', 'labelcolumn', 'onclick'.
those elements have the following types:
  - show (logical; optional)
  - name (character; optional)
  - color (character; optional)
  - sourcesize (numeric; optional)
  - shape (a value equal to: 'circle', "plus", "rhomb", 'cross', 'triangle', 'square'; optional)
  - maxnbsources (numeric; optional)
  - rafield (character; optional)
  - decfield (character; optional)
  - displaylabel (logical; optional)
  - labelcolor (character; optional)
  - labelfont (character; optional)
  - labelcolumn (character; optional)
  - onclick (a value equal to: 'showtable', 'showpopup'; optional) | lists containing elements 'type', 'data', 'options'.
those elements have the following types:
  - type (a value equal to: "overlay"; optional)
  - data (optional): . data has the following type: list of lists containing elements 'type', 'ra', 'dec', 'radius', 'color'.
those elements have the following types:
  - type (a value equal to: 'circle'; optional)
  - ra (numeric; optional)
  - dec (numeric; optional)
  - radius (numeric; optional)
  - color (character; optional) | lists containing elements 'type', 'data', 'color', 'linewidth'.
those elements have the following types:
  - type (a value equal to: 'polyline'; optional)
  - data (list of unnamed lists; optional)
  - color (character; optional)
  - linewidth (numeric; optional) | lists containing elements 'type', 'data'.
those elements have the following types:
  - type (a value equal to: 'polygon'; optional)
  - data (list of unnamed lists; optional)s
  - options (optional): . options has the following type: lists containing elements 'show', 'name', 'color', 'linewidth'.
those elements have the following types:
  - show (logical; optional)
  - name (character; optional)
  - color (character; optional)
  - linewidth (numeric; optional) | lists containing elements 'type', 'data', 'options'.
those elements have the following types:
  - type (a value equal to: 'moc'; optional)
  - data (character | named list; optional)
  - options (optional): . options has the following type: lists containing elements 'show', 'name', 'color', 'opacity', 'adaptativedisplay'.
those elements have the following types:
  - show (logical; optional)
  - name (character; optional)
  - color (character; optional)
  - opacity (numeric; optional)
  - adaptativedisplay (logical; optional)s. Layers to show.
Each layer can be one of types ['catalog', 'overlay', 'moc'].}

\item{objectClicked}{Named list. Clicked object.}

\item{objectHovered}{Named list. Hovered object.}

\item{options}{Named list. Additional options passed to the aladinlite.js}

\item{position}{Named list. Position.}

\item{style}{Named list. The style of the container.}

\item{survey}{Character | lists containing elements 'id', 'name', 'rooturl', 'cooframe', 'maxorder', 'options'.
those elements have the following types:
  - id (character; optional)
  - name (character; optional)
  - rooturl (character; optional)
  - cooframe (a value equal to: 'equatorial', 'galactic'; optional)
  - maxorder (numeric; optional)
  - options (optional): . options has the following type: lists containing elements 'imgformat'.
those elements have the following types:
  - imgformat (a value equal to: 'jpeg', 'fits', 'png'; optional). The survey to display as base image layer.}

\item{target}{Character. The target to display.}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

