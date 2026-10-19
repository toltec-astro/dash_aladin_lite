"""Aladin Lite sky atlas as a Dash component."""

from importlib.metadata import version

from ._imports_ import AladinLite
from .layers import (
    CatalogLayer,
    Circle,
    Degrees,
    EntityId,
    GraphicLayer,
    ImageLayer,
    Layer,
    Polygon,
    Polyline,
    Shape,
    SkyPosition,
    SkyPositions,
    Source,
)

__all__ = [
    "AladinLite",
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

__version__ = version(__name__)

_js_dist = [
    {
        "relative_package_path": "dash_aladin_lite.js",
        "namespace": __name__,
    },
    # Prop type checks for the TypeScript component, in Dash debug mode.
    {
        "dev_package_path": "proptypes.js",
        "dev_only": True,
        "namespace": __name__,
    },
]
