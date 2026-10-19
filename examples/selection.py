"""Sky view and table sharing one selection.

Each galaxy of the M81 group is a table row, a marker at its center and a box
around it, all with the row's id. Selecting rows, markers or boxes selects the
same galaxies in both views. Positions are approximate.

Run with ``python examples/selection.py`` and open http://127.0.0.1:8050.
"""

import astropy.units as u
import dash_ag_grid as dag
from astropy.coordinates import SkyCoord
from dash import Dash, Input, Output, ctx, html, no_update

from dash_aladin_lite import (
    AladinLite,
    CatalogLayer,
    GraphicLayer,
    Polygon,
    Source,
)

GALAXIES = [
    {"id": "m81", "name": "M81", "ra": 148.888, "dec": 69.065},
    {"id": "m82", "name": "M82", "ra": 148.968, "dec": 69.680},
    {"id": "ngc3077", "name": "NGC 3077", "ra": 150.829, "dec": 68.734},
    {"id": "ngc2976", "name": "NGC 2976", "ra": 146.815, "dec": 67.916},
]
BOX_HALF_SIZE = 0.15 * u.deg


def make_box(center: SkyCoord) -> SkyCoord:
    """Return the corners of a box around a position."""
    d = BOX_HALF_SIZE
    return center.spherical_offsets_by([-d, d, d, -d], [-d, -d, d, d])


centers = SkyCoord(
    [g["ra"] for g in GALAXIES], [g["dec"] for g in GALAXIES], unit="deg"
)
layers = [
    GraphicLayer(
        id="boxes",
        name="Boxes",
        color="#4dabf7",
        line_width=2,
        shapes=[
            Polygon(id=g["id"], vertices=make_box(c))
            for g, c in zip(GALAXIES, centers, strict=True)
        ],
    ),
    CatalogLayer(
        id="centers",
        name="Centers",
        color="#ff922b",
        shape="cross",
        source_size=14,
        sources=[Source(id=g["id"], ra=g["ra"], dec=g["dec"]) for g in GALAXIES],
    ),
]

app = Dash(__name__)
app.layout = html.Div(
    [
        AladinLite(
            id="sky",
            target="149.5 68.8",
            fov=3,
            layers=layers,
            options={"showContextMenu": True},
            style={"height": "480px"},
        ),
        dag.AgGrid(
            id="table",
            rowData=GALAXIES,
            columnDefs=[{"field": f} for f in ("name", "ra", "dec")],
            getRowId="params.data.id",
            dashGridOptions={"rowSelection": {"mode": "multiRow"}},
            style={"height": "220px"},
        ),
        html.Pre(id="selected"),
    ],
    style={"display": "grid", "gap": "12px", "padding": "12px"},
)


@app.callback(
    Output("sky", "selected_ids"),
    Output("table", "selectedRows"),
    Output("selected", "children"),
    Input("sky", "selected_ids"),
    Input("table", "selectedRows"),
)
def sync_selection(
    selected_ids: list[str] | None, selected_rows: list[dict] | None
) -> tuple:
    """Pass a selection made in one view to the other."""
    # Update only the other view: the grid reports any selection it is given
    # as a new value, which would trigger this callback again.
    if ctx.triggered_id == "table":
        ids = [row["id"] for row in selected_rows or []]
        return ids, no_update, f"selected_ids: {ids}"
    ids = selected_ids or []
    return no_update, {"ids": ids}, f"selected_ids: {ids}"


if __name__ == "__main__":
    app.run(debug=True)
