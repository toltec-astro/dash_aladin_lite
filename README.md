# dash_aladin_lite

[Aladin Lite](https://aladin.cds.unistra.fr/AladinLite/) v3 sky atlas as a
[Dash](https://dash.plotly.com/) component. Layers are given as data, and the
selection is a property shared with the rest of the app, so a table and the
sky view can highlight the same rows.

```python
from dash import Dash
from dash_aladin_lite import AladinLite, CatalogLayer, Source

app = Dash()
app.layout = AladinLite(
    id="sky",
    target="M82",
    fov=0.5,
    layers=[
        CatalogLayer(
            id="targets",
            sources=[Source(id="M82", ra=148.968, dec=69.680)],
        )
    ],
    style={"height": "480px"},
)
```

## Properties

| Property | Description |
| --- | --- |
| `target` | View center: an object name or `"ra dec"` in degrees. |
| `fov` | Field of view, in degrees. |
| `survey` | Base HiPS survey, e.g. `"P/DSS2/color"`. |
| `options` | Aladin Lite options used when the viewer is created. |
| `layers` | Layers drawn over the survey (below). |
| `selected_ids` | Ids of the selected entities; set by clicks and region selections, and settable from callbacks. |

## Layers

Layers are Pydantic models in `dash_aladin_lite.layers`; each has a unique
`id`. Positions are ICRS degrees, or astropy `SkyCoord` objects; angles are
degrees, or angular astropy quantities.

| Layer | Content |
| --- | --- |
| `ImageLayer` | A FITS image by URL (also a `data:` or `blob:` URL), with colormap and opacity, drawn over the survey or replacing it as the base image (`base=True`). |
| `CatalogLayer` | `Source` markers, each with an id. |
| `GraphicLayer` | `Polyline`, `Polygon` and `Circle` shapes, optionally with ids. |

Ids name entities, not drawn objects: a marker and a polygon drawn for the
same table row share its id, so selecting either one selects the row, and
selecting the row highlights both. Callbacks receive layers as dicts;
validate them with `pydantic.TypeAdapter(list[Layer])`.

## Example

`examples/selection.py` links the sky view and an AG Grid table:

```console
uv run --group example python examples/selection.py
```

## Development

The built component (`src/dash_aladin_lite/dash_aladin_lite.js`) and the generated
Python class are committed, so installing the package needs no Node.js. After
changing `src/ts/`, rebuild with Node.js and the package's Python environment
on `PATH` (for `dash-generate-components`):

```console
npm install
npm run build
```

The bundle includes Aladin Lite 3.8.2 from npm, which is distributed under the
GPL-3/LGPL-3 licenses.
