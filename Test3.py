import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_float import *

# Load the data
df = pd.read_csv("dataoutlet.csv")

# Ensure latitude and longitude are numeric
df["OUTLET_LATITUDE"] = pd.to_numeric(df["OUTLET_LATITUDE"])
df["OUTLET_LONGITUDE"] = pd.to_numeric(df["OUTLET_LONGITUDE"])

# Set your Mapbox access token
px.set_mapbox_access_token("pk.eyJ1IjoidGhlZG8zMiIsImEiOiJjbHMxbGRvaDEwYm5yMmtxeGZjenJ1ZnplIn0.HrgG-gRUV-3r4A0qv_Ozaw")

# Create a simple scatter mapbox plot
fig = px.scatter_mapbox(
    df,
    lat="OUTLET_LATITUDE",
    lon="OUTLET_LONGITUDE",
    size="SIZE",
    hover_name="BRAND",
    height=600,
    zoom=13,
    center={"lat": -0.9497, "lon": 100.3505}
)

fig.update_traces(cluster=dict(enabled=True))

st.plotly_chart(fig)
