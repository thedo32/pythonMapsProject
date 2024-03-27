import streamlit as st
from io import StringIO
import folium
from streamlit_float import *
import pandas as pd
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    #st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    #st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    #st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    #dataframe = pd.read_csv(uploaded_file)

    # draw basemap
    m = folium.Map(location=[-3.1940, 117.5540],
                   tiles='cartodbdarkmatter',
                   zoom_start=2, control_scale=True)

    if st.checkbox("Tampilkan Hotspot? Don't bother, make or order your coffee while loading"):
        points = pd.read_csv(uploaded_file)

        # Get x and y coordinates for each point
        # points_gjson = folium.features.GeoJson(points, name="Hotspot Indonesia")
        # points_gjson.add_to(m)
        # Get x and y coordinates for each point
        # points = pd.read_csv('maps/idns.csv')

        # Extract latitude and longitude columns
        marker_cluster = MarkerCluster()
        for _, row in points.iterrows():
            popup = f"Latitude: {row['Latitude']}<br>Longitude: {row['Longitude']}"
            folium.Marker([row['Latitude'], row['Longitude']], popup=popup).add_to(marker_cluster)

        marker_cluster.add_to(m)

    # Add maps to streamlit
        st.write("Jumlah Hotspot: " + str(len(points)))
    st_folium(m, height=450, use_container_width=True)