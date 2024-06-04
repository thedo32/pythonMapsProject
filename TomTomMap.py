import folium
import streamlit as st
from streamlit_folium import st_folium

TomTom_map = folium.Map(
    location=[45.523, -122.675],
    zoom_start=10,
    tiles= 'http://{s}.api.tomtom.com/map/1/tile/basic/main/{z}/{x}/{y}.png?'
           'view=e67b6e8b-2dc9-4a67-8d82-8c4ad6a8b3cc'
            ,attr='TomTom')

st_folium(TomTom_map)