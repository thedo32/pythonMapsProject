import folium
import geopandas as gpd
import pandas as pd
import streamlit
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

points = gpd.read_file('data/idns.geojson')
m = folium.Map(location=[-3.1940,117.5540], tiles = 'cartodbdarkmatter', zoom_start=4, control_scale=True)


# Get x and y coordinates for each point

points_gjson = folium.features.GeoJson(points, name="Hotspot Indonesia")
# points_gjson.add_to(m)

# Get x and y coordinates for each point
points["x"] = points["geometry"].x
points["y"] = points["geometry"].y

# Create a list of coordinate pairs
locations = list(zip(points["y"], points["x"]))

# Create a folium marker cluster
marker_cluster = MarkerCluster(locations)

# Add marker cluster to map
marker_cluster.add_to(m)

st_folium(m, use_container_width=True)