"""Layers of the Aladin Lite view.

A layer is data: a model here validates it and serializes it to the JSON that
:class:`~dash_aladin_lite.AladinLite` draws. Models can be passed directly as
the ``layers`` property; callbacks receive the layers back as dicts, which
:data:`Layer` validates again.

Positions are ICRS right ascension and declination in degrees. Fields that take
positions also accept an `~astropy.coordinates.SkyCoord`, and angles accept an
angular `~astropy.units.Quantity`.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

__all__ = [
    "CatalogLayer",
    "Circle",
    "Degrees",
    "EntityId",
    "GraphicLayer",
    "ImageLayer",
    "Layer",
    "Polygon",
    "Polyline",
    "Shape",
    "SkyPosition",
    "SkyPositions",
    "Source",
]


def _degrees(value: object) -> object:
    if isinstance(value, u.Quantity):
        return value.to_value(u.deg)
    return value


def _sky_position(value: object) -> object:
    if isinstance(value, SkyCoord):
        icrs = value.icrs
        return (icrs.ra.degree, icrs.dec.degree)
    return value


def _sky_positions(value: object) -> object:
    if isinstance(value, SkyCoord):
        icrs = value.icrs
        return np.column_stack(
            [np.atleast_1d(icrs.ra.degree), np.atleast_1d(icrs.dec.degree)]
        ).tolist()
    return value


type Degrees = Annotated[float, BeforeValidator(_degrees)]
"""Angle in degrees; an angular `~astropy.units.Quantity` is converted."""

type SkyPosition = Annotated[
    tuple[Degrees, Annotated[Degrees, Field(ge=-90, le=90)]],
    BeforeValidator(_sky_position),
]
"""``(ra, dec)`` in degrees (ICRS); a scalar `~astropy.coordinates.SkyCoord`
is converted."""

type SkyPositions = Annotated[list[SkyPosition], BeforeValidator(_sky_positions)]
"""List of ``(ra, dec)`` in degrees (ICRS); a `~astropy.coordinates.SkyCoord`
array is converted."""

type EntityId = str | int
"""Identifier of an entity, such as a table row; objects drawn for the same
entity share it."""


class _LayerModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    def to_plotly_json(self) -> dict[str, Any]:
        """Return the JSON value of the model.

        Dash calls this when the model is a component property. Unset optional
        fields are left out, so that Aladin Lite's defaults apply.

        Returns
        -------
        dict
            The model as JSON-compatible data.
        """
        return self.model_dump(mode="json", exclude_none=True)


class Source(_LayerModel):
    """Catalog source."""

    id: EntityId
    """Entity of the source."""

    ra: Degrees
    """Right ascension, in degrees (ICRS)."""

    dec: Annotated[Degrees, Field(ge=-90, le=90)]
    """Declination, in degrees (ICRS)."""


class Polyline(_LayerModel):
    """Open line through sky positions."""

    type: Literal["polyline"] = "polyline"
    id: EntityId | None = None
    """Entity of the line; a line without one cannot be selected."""

    vertices: SkyPositions
    """Vertices in drawing order."""


class Polygon(_LayerModel):
    """Closed polygon through sky positions."""

    type: Literal["polygon"] = "polygon"
    id: EntityId | None = None
    """Entity of the polygon; a polygon without one cannot be selected."""

    vertices: SkyPositions
    """Vertices in drawing order; the last one connects to the first."""


class Circle(_LayerModel):
    """Circle on the sky."""

    type: Literal["circle"] = "circle"
    id: EntityId | None = None
    """Entity of the circle; a circle without one cannot be selected."""

    center: SkyPosition
    """Center of the circle."""

    radius: Annotated[Degrees, Field(gt=0)]
    """Radius, in degrees."""


type Shape = Annotated[Polyline | Polygon | Circle, Field(discriminator="type")]
"""Shape of a graphic layer, chosen by its ``type``."""


class ImageLayer(_LayerModel):
    """FITS image drawn over the survey.

    Examples
    --------
    >>> layer = ImageLayer(id="coverage", url="coverage.fits", base=True)
    >>> layer.to_plotly_json()
    {'type': 'image', 'id': 'coverage', 'url': 'coverage.fits', 'base': True}
    """

    type: Literal["image"] = "image"
    id: str
    """Layer identifier, unique in the view."""

    name: str | None = None
    """Name shown in the layer control; defaults to `id`."""

    url: str
    """URL of the FITS file, which may be a ``data:`` URL."""

    colormap: str | None = None
    """Aladin Lite colormap name, e.g. ``"viridis"``."""

    opacity: Annotated[float, Field(ge=0, le=1)] | None = None
    """Opacity of the image."""

    base: bool = False
    """Whether the image replaces the survey as the base image of the view,
    until the layer is removed; at most one layer should set it."""


class CatalogLayer(_LayerModel):
    """Sources drawn as markers.

    Examples
    --------
    >>> layer = CatalogLayer(
    ...     id="targets",
    ...     sources=[Source(id="M82", ra=148.968, dec=69.680)],
    ... )
    >>> layer.to_plotly_json()["sources"]
    [{'id': 'M82', 'ra': 148.968, 'dec': 69.68}]
    """

    type: Literal["catalog"] = "catalog"
    id: str
    """Layer identifier, unique in the view."""

    name: str | None = None
    """Name shown in the layer control; defaults to `id`."""

    color: str | None = None
    """Marker color, as a CSS color."""

    shape: Literal["square", "circle", "plus", "cross", "rhomb", "triangle"] | None = (
        None
    )
    """Marker shape."""

    source_size: Annotated[int, Field(gt=0)] | None = None
    """Marker size, in screen pixels."""

    sources: list[Source]
    """Sources of the catalog."""

    visible: bool = True
    """Whether the layer is shown initially."""


class GraphicLayer(_LayerModel):
    """Lines, polygons and circles.

    Examples
    --------
    >>> import astropy.units as u
    >>> layer = GraphicLayer(
    ...     id="beam",
    ...     shapes=[Circle(center=(148.968, 69.680), radius=5 * u.arcsec)],
    ... )
    >>> layer.shapes[0].radius * 3600
    5.0
    """

    type: Literal["graphic"] = "graphic"
    id: str
    """Layer identifier, unique in the view."""

    name: str | None = None
    """Name shown in the layer control; defaults to `id`."""

    color: str | None = None
    """Line color, as a CSS color."""

    line_width: Annotated[float, Field(gt=0)] | None = None
    """Line width, in screen pixels."""

    shapes: list[Shape]
    """Shapes of the layer."""

    visible: bool = True
    """Whether the layer is shown initially."""


type Layer = Annotated[
    ImageLayer | CatalogLayer | GraphicLayer, Field(discriminator="type")
]
"""Layer of the view, chosen by its ``type``."""
