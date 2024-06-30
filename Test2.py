import streamlit as st
import plotly.express as px
import pandas as pd
import math


# Mock function to get data (replace with your actual data fetching function)
def fetch_data():
    df = pd.read_csv('dataoutlet.csv')
    additional_data = [{"text": "2142", "lat": -3.47, "lon": 105.96, "radius": 6000}]
    zoom_level = 8
    return df, additional_data, zoom_level


# Function to create the map
def create_map(df, center_lat, center_lon, zoom_level):
    fig = px.scatter_mapbox(
        df,
        lat="OUTLET_LATITUDE",
        lon="OUTLET_LONGITUDE",
        size="SIZE",
        mapbox_style="open-street-map",
        labels={"BRAND": "Brand"},
        hover_name="BRAND",
        hover_data=["BRANCH", "OUTLET_NAME", "RETAILER_QR_CODE", "NEAREST_SITE"],
        color="LEGEND",
        color_discrete_sequence=["darkgreen", "magenta"],
        height=600,
        zoom=zoom_level,
        center={"lat": center_lat, "lon": center_lon},
    )
    fig.update_layout(clickmode='event+select')
    return fig


# Function to calculate distance
def calculate_distance(lat1, lon1, lat2, lon2):
    r = 6371.0  # Radius of the Earth in kilometers
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = r * c
    return distance


# Callback function for the selection event
def on_select(event):
    if 'click_count' not in st.session_state:
        st.session_state.click_count = 0
        st.session_state.lat1 = None
        st.session_state.lon1 = None
        st.session_state.lat2 = None
        st.session_state.lon2 = None

    point = event['points'][0]
    lat = point['lat']
    lon = point['lon']

    if st.session_state.click_count == 0:
        st.session_state.lat1 = lat
        st.session_state.lon1 = lon
        st.session_state.click_count += 1
    elif st.session_state.click_count == 1:
        st.session_state.lat2 = lat
        st.session_state.lon2 = lon
        st.session_state.click_count += 1


# Streamlit app
if __name__ == "__main__":
    loc = {'coords': {'latitude': -3.47, 'longitude': 105.96}}  # Example location data

    if loc:
        latitude = loc['coords']['latitude']
        longitude = loc['coords']['longitude']

        st.write(f"Koordinat Lokasi Anda, Lat: {latitude}, Lon: {longitude}")

        df, additional_data, zoom_level = fetch_data()
        fig = create_map(df, latitude, longitude, zoom_level)

        # Track click events and store coordinates in session state
        event = st.plotly_chart(fig, use_container_width=True, on_select=on_select)

        if st.session_state.lat1 and st.session_state.lon1:
            st.write(f"First point: Lat: {st.session_state.lat1}, Lon: {st.session_state.lon1}")

        if st.session_state.lat2 and st.session_state.lon2:
            st.write(f"Second point: Lat: {st.session_state.lat2}, Lon: {st.session_state.lon2}")
            distance = calculate_distance(st.session_state.lat1, st.session_state.lon1, st.session_state.lat2,
                                          st.session_state.lon2)
            st.write(f"Distance: {distance:.2f} km")

        with st.expander("Hitung Jarak"):
            if st.session_state.lat1 and st.session_state.lon1 and st.session_state.lat2 and st.session_state.lon2:
                distance = calculate_distance(st.session_state.lat1, st.session_state.lon1, st.session_state.lat2,
                                              st.session_state.lon2)
                st.write(f"Distance between selected points: {distance:.2f} km")
