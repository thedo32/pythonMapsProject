import streamlit as st
from streamlit_float import *
import pandas as pd
import plotly.express as px
import fungsi as fu

st.set_page_config(
    page_title="Hotspot Kebakaran Lahan Hutan dan Polusi Udara",
    page_icon="fishtail.png",
    layout="wide",
    menu_items={"About": """##### Pengaruh Hotspot Di Musim El Nino Oktober 2023 Terhadap Generasi Masa Depan. 
            Author: Jeffri Argon
Email: jeffriargon@gmail.com
            """}
)

color_dic = {"3ID":'magenta',"IM3":"yellow"}

df = fu.wilayah_admin("Kota Palembang")
# Create the choropleth bubble map
fig = px.scatter_mapbox(
    df[0],
    lat="OUTLET_LATITUDE",
    lon="OUTLET_LONGITUDE",
    size="SIZE",
    mapbox_style="carto-darkmatter",  # Choose a suitable projection
    labels={"BRAND"},
    hover_name="BRAND",  # Display count on hover
    hover_data=["BRANCH","OUTLET_NAME", "RETAILER_QR_CODE","NEAREST_SITE"],
    color="LEGEND",
    color_discrete_sequence=["yellow","yellow","yellow","yellow",
                             "magenta","magenta","magenta","magenta","magenta","magenta"],
    height=600,
    zoom=df[2],
    center=dict(lat=df[3], lon=df[4]),  # this will center on the point
)

# Show the map
st.plotly_chart(fig, use_container_width=True)
