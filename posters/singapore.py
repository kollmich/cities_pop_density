# NUTS2 Indicators
# Michal Kollar, July 2020
#.shp conversion to .geojson --all supplementing files (.dbf etc..) must be present in the folder where the conversion is taking place
# ogr2ogr -f GeoJSON -t_srs crs:84 [name].geojson [name].shp

# GEO (2014) = https://data.gov.sg/dataset/master-plan-2014-planning-area-boundary-web
# DATA (2020) = https://www.citypopulation.de/en/singapore/admin/


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

pio.kaleido.scope.default_format = "png"
pio.kaleido.scope.default_width = 4800 #4960
pio.kaleido.scope.default_height = 4800 #3508
pio.kaleido.scope.default_scale = 1
pio.kaleido.scope.mapbox_access_token = "pk.eyJ1Ijoia29sbDQ0IiwiYSI6ImNrZG94Ym9taDF3bDIycHEzdGs0cm4zNWkifQ.vC69MtmQObqmG4XJfxG6bw"

custom_style = "mapbox://styles/koll44/ckfv78o6h0o8r1amuahfnuhyb"
custom_style = "mapbox://styles/koll44/ckf79bo7f1gwi19mi4e6plhdi"

geo_file = "geojson/Singapore/singapore.geojson"

df = geopandas.read_file(geo_file)
# df = df.to_csv("singapore.csv")
data = pd.read_csv('data/singapore.csv', encoding = "utf-8", sep =';')#ISO-8859-1
data['level_2'] = data['level_2'].str.upper()

# join the geodataframe with the csv dataframe
merged = df.merge(data, how='left', left_on="PLN_AREA_N", right_on="level_2")
#merged = merged[['Code', 'geometry', 'Borough', 'Ward_Name', 'Year', 'Population', 'Hectares', 'Square_Kilometres', 'Population_per_hectare', 'Population_per_square_kilometre']]
print(merged)
merged.to_file("singapore_id.geojson", driver='GeoJSON')

with open("singapore_id.geojson") as jsonfile:
    final = json.load(jsonfile)

for i in final['features']:
    i['id'] = i['properties']['PLN_AREA_C']

if os.path.exists("singapore_final.geojson"):
    os.remove("singapore_final.geojson")
else:
    print('file doesn''t exist')

with open("singapore_final.geojson", "w") as jsonFileFinal:
    json.dump(final, jsonFileFinal)

jsonfile.close()
jsonFileFinal.close()


with open('singapore_final.geojson') as json_file:
    singapore = json.load(json_file)


custom_style = "mapbox://styles/koll44/ckf79bo7f1gwi19mi4e6plhdi"

fig = go.Figure(go.Choroplethmapbox(
    geojson=singapore,
    locations=merged['PLN_AREA_C'], # Spatial coordinates
    z = merged['density'], # Data to be color-coded
    # locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale=[[0, '#ffc33e'], [0.5, '#ff0000'], [1, '#000']], zmin=0,zmax=30000,
    marker_opacity=0.65, marker_line_width=1.5,marker_line_color='#fff',text=merged['PLN_AREA_N']
))


# fig.update_layout(mapbox_style="carto-positron",
#                   mapbox_zoom=3, mapbox_center = {"lat": 0, "lon": 50})

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
                    zoom=12.6,
                    center= dict(lat=1.345,
                                    lon=103.845),
                    )
                  )

fig.update_layout(margin={"r":100,"t":100,"l":100,"b":100})
fig.show()


if not os.path.exists("images"):
    os.mkdir("images")

# original
fig.write_image("images/singapore.png", engine="kaleido")
print("image saved")

server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
external_stylesheets = ['https://codepen.io/majkl65/pen/LYpVxEP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)

app.layout = html.Div([
    html.H1(children='● MAP PROJECTIONS',
            className='header'),

    html.P(
        "Different Ways of Flattening the Globe's Surface.",
        className='subheader',
    ),
    dcc.Graph(
        id='fig_1',
        config={
            'displayModeBar': False,
            'displaylogo': False,
            'modeBarButtonsToRemove': ["zoom2d", "pan2d", "select2d", "lasso2d", "autoScale2d", "hoverClosestCartesian", "hoverCompareCartesian", "zoom3d", "pan3d", "resetCameraDefault3d", "resetCameraLastSave3d", "hoverClosest3d", "orbitRotation", "tableRotation","resetGeo", "hoverClosestGeo", "sendDataToCloud", "hoverClosestGl2d", "hoverClosestPie", "toggleHover", "toggleSpikelines"]
            #'modeBarButtonsToRemove': ["zoom2d", "pan2d", "select2d", "lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d", "hoverClosestCartesian", "hoverCompareCartesian", "zoom3d", "pan3d", "resetCameraDefault3d", "resetCameraLastSave3d", "hoverClosest3d", "orbitRotation", "tableRotation", "zoomInGeo", "zoomOutGeo", "resetGeo", "hoverClosestGeo", "toImage", "sendDataToCloud", "hoverClosestGl2d", "hoverClosestPie", "toggleHover", "resetViews", "toggleSpikelines", "resetViewMapbox"]
        },
        figure=fig
    ),

    html.P(
        "data: yifysubtitles.com",
        className='dataheader',
    ),
    html.P(
        "trendspotting.site",
        className='brandheader',
    )
])

if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
