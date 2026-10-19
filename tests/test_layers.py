import astropy.units as u
import numpy as np
import pytest
from astropy.coordinates import SkyCoord
from pydantic import TypeAdapter, ValidationError

from dash_aladin_lite import (
    CatalogLayer,
    Circle,
    GraphicLayer,
    ImageLayer,
    Layer,
    Polygon,
    Polyline,
    Source,
)

M82 = SkyCoord("09h55m52.4s +69d40m47s")


def test_positions_from_skycoord_are_icrs_degrees() -> None:
    galactic = M82.galactic
    circle = Circle(center=galactic, radius=1 * u.arcmin)
    assert circle.center == pytest.approx((M82.ra.degree, M82.dec.degree))
    assert circle.radius == pytest.approx(1 / 60)
    corners = SkyCoord([148.9, 149.0, 149.0] * u.deg, [69.6, 69.6, 69.7] * u.deg)
    polygon = Polygon(vertices=corners.galactic)
    assert np.asarray(polygon.vertices) == pytest.approx(
        np.asarray([(148.9, 69.6), (149.0, 69.6), (149.0, 69.7)])
    )


def test_angles_need_angular_units() -> None:
    with pytest.raises(ValidationError, match="radius"):
        Circle(center=(0, 0), radius=1 * u.m)
    with pytest.raises(ValidationError, match="dec"):
        Source(id=1, ra=0, dec=91)


def test_json_leaves_out_unset_styles() -> None:
    layer = GraphicLayer(
        id="boxes",
        color="#4dabf7",
        shapes=[Polygon(id="a", vertices=[(1, 2), (3, 4), (5, 6)])],
    )
    assert layer.to_plotly_json() == {
        "type": "graphic",
        "id": "boxes",
        "color": "#4dabf7",
        "shapes": [
            {"type": "polygon", "id": "a", "vertices": [[1, 2], [3, 4], [5, 6]]}
        ],
        "visible": True,
    }


def test_layers_validate_back_from_callback_dicts() -> None:
    layers = [
        ImageLayer(id="coverage", url="data:application/fits;base64,", opacity=0.7),
        ImageLayer(id="map", url="blob:http://localhost/1", base=True),
        CatalogLayer(id="centers", sources=[Source(id=7, ra=1, dec=2)]),
        GraphicLayer(
            id="paths",
            shapes=[
                Polyline(vertices=[(1, 2), (3, 4)]),
                Circle(id="b", center=(1, 2), radius=0.1),
            ],
            visible=False,
        ),
    ]
    data = [layer.to_plotly_json() for layer in layers]
    assert TypeAdapter(list[Layer]).validate_python(data) == layers


def test_layer_fields_are_checked() -> None:
    with pytest.raises(ValidationError, match="extra_forbidden"):
        TypeAdapter(Layer).validate_python(
            {"type": "catalog", "id": "a", "sources": [], "colour": "red"}
        )
    with pytest.raises(ValidationError, match="union_tag_invalid"):
        TypeAdapter(Layer).validate_python({"type": "moc", "id": "a"})
