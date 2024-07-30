import base64
import time
from dotenv import load_dotenv
import os
import mesop as me
import mesop.labs as mel
import streamlit as st
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import fungsiumum as fu
import fungsipeta as fp
from geopy.geocoders import Nominatim
import plotly.io as pio

@me.stateclass
class State:
    checked: bool

def on_update(event: me.CheckboxChangeEvent):
    state = me.state(State)
    state.checked = event.checked

@me.page()
@me.page(
security_policy=me.SecurityPolicy(
     allowed_iframe_parents=["https://google.github.io"]
   ),
   path="/embed",
 )
def app():
    state = me.state(State)
    me.checkbox(
        "Tentukan Lokasi Anda",
        on_change=on_update,
    )

    if state.checked:
        loc = Nominatim(user_agent="MesopMap")
        getLoc = loc.geocode("Padang Utara, Kota Padang, Sumatra Barat")

        if getLoc:
            latitude = getLoc.latitude
            longitude = getLoc.longitude

            me.text(f"Koordinat Lokasi Anda, Lat: {latitude}, Lon: {longitude}")

            fig = fp.addmap(latitude, longitude, 13, "maps/output.parquet")

            try:
                # Save Plotly figure to an HTML file
                file_path = "map.html"
                pio.write_html(fig, file_path, full_html=True, include_plotlyjs="cdn")
                me.text("Map saved successfully to HTML file.")
                src = "http://localhost:63342/pythonMapsProject/map.html?_ijt=qbvee6t6gapnu09jruj3idhjfc&_ij_reload=RELOAD_ON_SAVE"

                me.text("Embedding: " + src)
                me.embed(
                    src=src,
                    style=me.Style(width="100%", height="600px"),
                )

            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                me.text(error_message)
                raise
