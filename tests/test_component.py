import json
from importlib.resources import files

from dash import Dash, html
from dash._utils import to_json

from dash_aladin_lite import AladinLite, CatalogLayer, Source


def test_models_serialize_as_layer_props() -> None:
    layer = CatalogLayer(id="centers", sources=[Source(id="a", ra=1, dec=2)])
    component = AladinLite(id="sky", layers=[layer], selected_ids=["a"])
    props = json.loads(to_json(component))["props"]
    assert props["layers"] == [layer.to_plotly_json()]
    assert props["selected_ids"] == ["a"]


def test_app_serves_the_component_bundle() -> None:
    app = Dash(__name__)
    app.layout = html.Div(AladinLite(id="sky"))
    client = app.server.test_client()
    # The renderer loads the bundle from the page's script list.
    index = client.get("/").get_data(as_text=True)
    assert "_dash-component-suites/dash_aladin_lite/dash_aladin_lite.v" in index
    response = client.get(
        "/_dash-component-suites/dash_aladin_lite/dash_aladin_lite.js"
    )
    assert response.status_code == 200
    bundle = files("dash_aladin_lite") / "dash_aladin_lite.js"
    assert response.get_data() == bundle.read_bytes()
