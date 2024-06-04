import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import streamlit as st

# Set the XKCD style
plt.xkcd()

# Title of the Streamlit app
st.title('Interactive XKCD Style World Map')

# Sidebar for user input
st.sidebar.header('User Input Features')

# Latitude and Longitude sliders
lat = st.sidebar.slider('Latitude', -90.0, 90.0, 0.0)
lon = st.sidebar.slider('Longitude', -180.0, 180.0, 0.0)

# Plotting function
def plot_map(lat, lon):
    fig = plt.figure(figsize=(10, 5))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Add the map with coastlines
    ax.coastlines()
    ax.gridlines(draw_labels=True)

    # Adding a scatter plot with the given latitude and longitude
    ax.scatter(lon, lat, color='blue', s=100, transform=ccrs.PlateCarree())

    # Adding labels and title
    plt.title('Interactive XKCD Style World Map')

    return fig

# Generate the map with the current latitude and longitude
fig = plot_map(lat, lon)

# Display the map using Streamlit
st.pyplot(fig)
