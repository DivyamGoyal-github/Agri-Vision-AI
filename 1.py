import folium
import ee
import matplotlib.pyplot as plt
import seaborn as sns
import IPython.display as disp
from branca.element import Figure
import numpy as np
from dotenv import load_dotenv  # added to load env variables
import os                       # added for env var support

load_dotenv(dotenv_path=".env.local")  # load env variables from .env.local

PROJECT_ID = os.environ.get("PROJECT_ID")  # get project id from env

ee.Authenticate()
ee.Initialize(project=PROJECT_ID)  # modified to load project id from .env.local
 
from folium import Map, Marker
from folium.plugins import MarkerCluster
from branca.element import Figure

fig1 = Figure(width=550, height=350)

map1 = Map(location=[11.777968, 76.597909], zoom_start=12, width=550, height=350)
fig1.add_child(map1)

Marker(
    location=[11.777968, 76.597909],
    popup='Default popup Marker1',
    tooltip='Click here to see Popup'
).add_to(map1)

fig1.save("map.html")
print("Map saved as map.html. Open it in your browser.")


watershed = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            [
              76.60413366762856,
              11.78151054870402
            ],
            [
              76.57344831024034,
              11.794260585249859
            ],
            [
              76.56196889596544,
              11.78161860234809
            ],
            [
              76.55622918882744,
              11.756549018691018
            ],
            [
              76.57377944719059,
              11.750713529259215
            ],
            [
              76.60567897339666,
              11.748119938711639
            ],
            [
              76.61450929206984,
              11.769840505010293
            ],
            [
              76.63261144534937,
              11.775243364615974
            ],
            [
              76.65866088543544,
              11.787885640990154
            ],
            [
              76.65369383118195,
              11.796853740543014
            ],
            [
              76.6294104548312,
              11.810359361287453
            ],
            [
              76.60413366762856,
              11.78151054870402
            ]
          ]
        ],
        "type": "Polygon"
      }
    }
  ]
}


from folium import Map, Marker, GeoJson
from branca.element import Figure

# Your base map setup
fig1 = Figure(width=550, height=350)
map1 = Map(location=[11.777968, 76.597909], zoom_start=12, width=550, height=350)
fig1.add_child(map1)

# Add the GeoJSON layer (assuming 'watershed' is valid GeoJSON data)
GeoJson(
    data=watershed,
    style_function=lambda x: {'fillColor': 'orange'}
).add_to(map1)

# Save instead of display
fig1.save("map.html")
print("✅ Map with GeoJSON layer saved as 'map.html'. Open it in your browser.")

ee.Initialize(project=PROJECT_ID)  # modified to load project id from .env.local

coords = watershed['features'][0]['geometry']['coordinates']
aoi = ee.Geometry.Polygon(coords)


image = ee.ImageCollection('COPERNICUS/S1_GRD').filterBounds(aoi).filterDate('2024-08-01', '2024-12-31').first().clip(aoi);
image.bandNames().getInfo()

url = image.select('VV').getThumbURL({'min': -20, 'max': 0})
disp.Image(url=url, width=800)
image.bandNames().getInfo()

url = image.select('VV').getThumbURL({'min': -20, 'max': 0})
disp.Image(url=url, width=800)

# image = ee.Image("COPERNICUS/S2/20220101T000239_20220101T000239_T56MNL")
# print(image.getInfo())


