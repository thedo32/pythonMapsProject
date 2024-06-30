import pandas as pd
import streamlit as st
from streamlit_float import *
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")


@st.cache_resource
def addmap(lat, lon,zm,fn):
    df = pd.read_parquet(fn)
    # Create the choropleth bubble map

    df["OUTLET_LATITUDE"] = pd.to_numeric(df["OUTLET_LATITUDE"])
    df["OUTLET_LONGITUDE"] = pd.to_numeric(df["OUTLET_LONGITUDE"])

    px.set_mapbox_access_token(MAPBOX_TOKEN)

    fig = px.scatter_mapbox(
        df,
        lat="OUTLET_LATITUDE",
        lon="OUTLET_LONGITUDE",
        size="SIZE",
        labels={"BRAND"},
        hover_name="BRAND",  # Display count on hover
        mapbox_style="open-street-map",  # Choose a suitable projection
        hover_data=["BRANCH", "OUTLET_NAME", "RETAILER_QR_CODE", "NEAREST_SITE"],
        color="LEGEND",
        color_discrete_sequence=["darkgreen", "darkgreen", "darkgreen", "darkgreen",
                                 "magenta", "magenta", "magenta", "magenta", "magenta", "magenta"],
        height=600,
        zoom=zm,
        center={"lat": lat, "lon": lon},  # this will center on the point
    )

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    return fig

def addmapcluster(lat, lon,zm,fn):
    df = pd.read_parquet(fn)
    # Create the choropleth bubble map

    df["OUTLET_LATITUDE"] = pd.to_numeric(df["OUTLET_LATITUDE"])
    df["OUTLET_LONGITUDE"] = pd.to_numeric(df["OUTLET_LONGITUDE"])

    px.set_mapbox_access_token(MAPBOX_TOKEN)

    fig = px.scatter_mapbox(
        df,
        lat="OUTLET_LATITUDE",
        lon="OUTLET_LONGITUDE",
        size="SIZE",
        labels={"BRAND"},
        hover_name="BRAND",  # Display count on hover
        hover_data=["BRANCH", "OUTLET_NAME", "RETAILER_QR_CODE", "NEAREST_SITE"],
        color="LEGEND",
        color_discrete_sequence=["darkgreen", "darkgreen", "darkgreen", "darkgreen",
                                 "magenta", "magenta", "magenta", "magenta", "magenta", "magenta"],
        height=800,
        zoom=zm,
        center={"lat": lat, "lon": lon},  # this will center on the point
    )

    fig.update_traces(cluster=dict(enabled=True))

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    return fig

def addmapkotakab(lat, lon,zm,fn):
    df = pd.read_parquet(fn)
    # Create the choropleth bubble map

    df["OUTLET_LATITUDE"] = pd.to_numeric(df["OUTLET_LATITUDE"])
    df["OUTLET_LONGITUDE"] = pd.to_numeric(df["OUTLET_LONGITUDE"])

    px.set_mapbox_access_token(MAPBOX_TOKEN)
    fig = px.scatter_mapbox(
        df,
        lat="OUTLET_LATITUDE",
        lon="OUTLET_LONGITUDE",
        size="SIZE",
        labels={"BRAND"},
        hover_name="BRAND",  # Display count on hover
        hover_data=["BRANCH", "OUTLET_NAME", "RETAILER_QR_CODE", "NEAREST_SITE"],
        color="LEGENDS",
        height=800,
        zoom=zm,
        center={"lat": lat, "lon": lon},  # this will center on the point
    )

    fig.update_traces(cluster=dict(enabled=True))

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    return fig