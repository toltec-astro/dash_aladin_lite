import dash_aladin_lite as dal
import dash
import dash_bootstrap_components as dbc
from dash import html, Input, Output, dcc
import pandas as pd
import yaml

app = dash.Dash(__name__)


sources = pd.DataFrame([
    [83.784490, 9.934156, 'Meissa', "Meissa", True],
    [88.792939, 7.407064, 'Betelgeuse', "Betelgeuse", True],
    [81.282764, 6.349703, 'Bellatrix', "Bellatrix", True]
    ], columns=['ra', 'dec', 'name', 'popupTitle', 'marker'])


app.layout = html.Div([
    dal.DashAladinLite(
        id='a',
        target='M51',
        fov=0.5,
        layers=[
            {
                "type": "catalog",
                "data": sources.to_dict(orient='records'),
                'options': {
                    "color": '#660066',
                    "name": "Three sources",
                    "show": True,
                    }
                },
            {
                "type": "catalog",
                "data": 'https://axel.u-strasbg.fr/HiPSCatService/SIMBAD',
                'options': {
                    "show": False,
                    "id": 'simbad',
                    "name": 'SIMBAD',
                    "shape": 'circle',
                    "sourceSize": 8,
                    "color": '#318d80',
                    # "onClick": "showPopup"
                    },
                },
            {
                "type": "overlay",
                "data": [
                    {
                        "type": "circle",
                        "ra": 83.66067,
                        "dec": 22.03081,
                        "radius": 0.04,
                        "color": 'cyan'
                        },
                    {
                        'type': "polygon",
                        "data": [
                            [83.64287, 22.01713],
                            [83.59872, 22.01692],
                            [83.59852, 21.97629],
                            [83.64295, 21.97629]],
                        },
                    {
                        "type": "polygon",
                        "data": [
                            [83.62807, 22.06330],
                            [83.58397, 22.02280],
                            [83.62792, 22.02258]],
                        },
                    ],
                'options': {
                    "show": True,
                    "color": '#ee2345',
                    "lineWidth": 3,
                    "name": "circle+polygon"
                    }
                },
            {
                "type": "overlay",
                "data": [
                    {
                        'type': "polyline",
                        "data": [
                            [2.29452158, 59.14978110],
                            [10.12683778, 56.53733116],
                            [14.1772154, 60.7167403],
                            [21.45396446, 60.23528403],
                            [28.59885697, 63.67010079]
                            ]
                        },
                    ],
                'options': {
                    "show": True,
                    "color": '#eee345',
                    "lineWidth": 2,
                    "name": "polyline"
                    }
                },

            {
                "type": "moc",
                "data": 'https://alasky.unistra.fr/MocServer/query?ivorn=ivo%3A%2F%2FCDS%2FV%2F139%2Fsdss9&get=moc&order=7&fmt=fits',
                'options': {
                    "show": False,
                    'color': '#84f',
                    'lineWidth': 1,
                    "name": "MOC from URL"
                    }
                },
            {
                "type": "moc",
                "data": {"3":[517],
"4":[2065,2066,2067,2112,2344,2346,2432],
"5":[8221,8257,8258,8259,8293,8304,8305,8307,8308,8452,8456,9346,9352,9354,9736],
"6":[32861,32862,32863,32881,32882,32883,32892,32893,33025,33026,33027,33157,33168,33169,33171,
33181,33224,33225,33227,33236,33240,33812,33816,33828,33832,37377,37378,37379,37382,37388,
37390,37412,37414,37420,37422,37562,38928,38930,38936,38948,38952],
"7":[131423,131439,131443,131523,131556,131557,131580,131581,132099,132612,132613,132624,132625,132627,132637,
132680,132681,132683,132709,132720,132721,132904,132905,132948,132952,132964,132968,133008,133009,133012,135252,135256,135268,135316,135320,135332,135336,148143,148152,148154,149507,149520
,149522,149523,149652,149654,149660,149662,149684,149686,149692,149694,149695,150120,150122,150208,150210,150216,150218,150240,150242,150243,155748,155752,155796,155800,155812,155816]},
                'options': {"show": False, 'opacity': 0.25, 'color': 'magenta', 'lineWidth': 1, "name": "MOC from JSON"}
                },
            ],
        options={
            # 'showAllskyRing': True,
            # 'showCooGrid': True,
            'showSimbadPointerControl': True,
            'showLayerBox': True,
            },
        survey={
            'id': 'P/Plank',
            'name': 'Plank',
            'rootUrl': 'http://alasky.cds.unistra.fr/PLANCK/R2/COM_CMB_IQU-smica-field-Int_2048_R2.00',
            'cooFrame': 'galactic',
            'maxOrder': 3,
            'options': {
                'imgFormat': 'png'
                }
            }
    ),
    dcc.Slider(0, 20, 1,
               value=10,
               id='s'
               ),
    dbc.Switch(
    id="sw",
    label="autoFov",
    value=False,
                ),
    dcc.Dropdown(
        options=[
            {
                'label': v,
                'value': v
                }
            for v in ["P/DSS2/color", "P/SDSS9/color"]
            ],
        value='P/SDSS9/color',
        id='sv'
        ),

    dcc.Dropdown(
        options=[
            {
                'label': v,
                'value': v
                }
            for v in ["M1", "M2", "M51"]
            ],
        value='M1',
        id='t'
        ),
    html.Pre(id='output'),
])


@app.callback(
    Output('a', 'fov'), [Input('s', 'value')])
def change_fov(fov_value):
    return fov_value


@app.callback(
    Output('a', 'autoFov'), [Input('sw', 'value')])
def change_auto_fov(autofov_value):
    return autofov_value


@app.callback(
    Output('a', 'survey'), [Input('sv', 'value')])
def change_survey(survey_value):
    return survey_value


@app.callback(
    Output('a', 'target'), [Input('t', 'value')])
def change_target(target_value):
    return target_value


@app.callback(
    Output('output', 'children'), inputs={
        k: Input('a', k)
        for k in [
            'id', 'className', 'style', 'target', 'fov', 'autoFov',
            'survey', 'options',
            'objectClicked', 'objectHovered',
            'footprintClicked', 'footprintHovered',
            'position',
            ]})
def display_output(**kwargs):
    return yaml.dump(kwargs)


if __name__ == '__main__':
    app.run_server(debug=True)
