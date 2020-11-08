# NUTS2 Indicators
# Michal Kollar, July 2020
#.shp conversion to .geojson --all supplementing files (.dbf etc..) must be present in the folder where the conversion is taking place
# ogr2ogr -f GeoJSON -t_srs crs:84 [name].geojson [name].shp

# GEO = https://data.cityofnewyork.us/City-Government/Neighborhood-Tabulation-Areas-NTA-/cpf4-rkhq
# DATA(2010) = https://data.cityofnewyork.us/City-Government/New-York-City-Population-By-Neighborhood-Tabulatio/swpk-hqdp

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json

import os
from random import randint
import flask

import geopandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.io as pio
# Pixels have been increased in size to match the short side requirement (2900px).
# Image far outside the recommended 1.4:1 ratio.
# Number of DPI less than 300.
# Logo, watermark, borders added.
# Text/content from the edge less than 200px for the file with min. size 4060px x 2900 px.

pio.kaleido.scope.default_format = "html"
pio.kaleido.scope.mapbox_access_token = "pk.eyJ1Ijoia29sbDQ0IiwiYSI6ImNrZG94Ym9taDF3bDIycHEzdGs0cm4zNWkifQ.vC69MtmQObqmG4XJfxG6bw"

custom_style = "mapbox://styles/koll44/ckfv78o6h0o8r1amuahfnuhyb"
custom_style = "mapbox://styles/koll44/ckf79bo7f1gwi19mi4e6plhdi"

data = pd.read_csv('../data/nyc.csv', encoding = "utf-8")#ISO-8859-1


with open('../geojson/FINAL/nyc_final.geojson') as json_file:
    nyc = json.load(json_file)


fig = go.Figure(go.Choroplethmapbox(
    geojson=nyc,
    locations=data['boro_cd'], # Spatial coordinates
    z = data['pop_density'], # Data to be color-coded
    # locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale=[[0, '#ffc33e'], [0.5, '#ff0000'], [1, '#000']], zmin=0,zmax=40000,
    marker_opacity=0.65, marker_line_width=1.5,marker_line_color='#fff',text=data['cb']
))

fig.update_layout(#mapbox_style="dark",
                #   width=4000, #4960,
                #   height=3700,
                  showlegend = True,
                  mapbox=dict(
                    accesstoken = "pk.eyJ1Ijoia29sbDQ0IiwiYSI6ImNrZG94Ym9taDF3bDIycHEzdGs0cm4zNWkifQ.vC69MtmQObqmG4XJfxG6bw",
                    style=custom_style,
                    # opacity=0.5
                    # bearing=10,
                    # pitch=60,
                    zoom=10,
                    center= dict(lat=40.7,
                                    lon=-73.977728),
                    )
                  )

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

# original
pio.write_html(fig, file='ny.html', auto_open=True)
print("html saved")


# server = flask.Flask(__name__)
# server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
# external_stylesheets = ['https://codepen.io/majkl65/pen/LYpVxEP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)

# app.layout = html.Div([
#     html.H1(children='● MAP PROJECTIONS',
#             className='header'),

#     html.P(
#         "Different Ways of Flattening the Globe's Surface.",
#         className='subheader',
#     ),
#     dcc.Graph(
#         id='fig_1',
#         config={
#             'displayModeBar': False,
#             'displaylogo': False,
#             'modeBarButtonsToRemove': ["zoom2d", "pan2d", "select2d", "lasso2d", "autoScale2d", "hoverClosestCartesian", "hoverCompareCartesian", "zoom3d", "pan3d", "resetCameraDefault3d", "resetCameraLastSave3d", "hoverClosest3d", "orbitRotation", "tableRotation","resetGeo", "hoverClosestGeo", "sendDataToCloud", "hoverClosestGl2d", "hoverClosestPie", "toggleHover", "toggleSpikelines"]
#             #'modeBarButtonsToRemove': ["zoom2d", "pan2d", "select2d", "lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d", "hoverClosestCartesian", "hoverCompareCartesian", "zoom3d", "pan3d", "resetCameraDefault3d", "resetCameraLastSave3d", "hoverClosest3d", "orbitRotation", "tableRotation", "zoomInGeo", "zoomOutGeo", "resetGeo", "hoverClosestGeo", "toImage", "sendDataToCloud", "hoverClosestGl2d", "hoverClosestPie", "toggleHover", "resetViews", "toggleSpikelines", "resetViewMapbox"]
#         },
#         figure=fig
#     ),

#     html.P(
#         "data: yifysubtitles.com",
#         className='dataheader',
#     ),
#     html.P(
#         "trendspotting.site",
#         className='brandheader',
#     )
# ])

# if __name__ == '__main__':
#     app.server.run(debug=True, threaded=True)
