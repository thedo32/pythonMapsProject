import base64
import time
import mesop as me
import mesop.labs as mel
from dotenv import load_dotenv
import os
import streamlit as st
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import fungsiumum as fu
import fungsipeta as fp
# importing geopy library
from geopy.geocoders import Nominatim
import plotly.io as pio




@me.stateclass
class State:
    checked: bool


def on_update(event: me.CheckboxChangeEvent):
    state = me.state(State)
    state.checked = event.checked


@me.page()
# @me.page(
#   security_policy=me.SecurityPolicy(
#     allowed_iframe_parents=["https://google.github.io"]
#   ),
#   path="/checkbox",
# )
def app():
    state = me.state(State)
    me.checkbox(
        "Tentukan Lokasi Anda",
        on_change=on_update,
    )

    if state.checked:
      # calling the Nominatim tool
      loc = Nominatim(user_agent="MesopMap")

      # entering the location name
      getLoc = loc.geocode("Padang Utara, Kota Padang, Sumatra Barat")


      if loc:
          latitude = getLoc.latitude
          longitude = getLoc.longitude

          me.text(f"Koordinat Lokasi Anda, Lat: " + str(latitude) + ", Lon: " + str(longitude))

          fig = fp.addmap(latitude, longitude, 13, "maps/output.parquet")

          try:
              # Save Plotly figure to an HTML file
              file_path = "map.html"
              pio.write_html(fig, file_path, full_html=False, auto_open=True, auto_play=True)
              me.text("Map saved successfully to HTML file.")

              # Embed the HTML file
              me.embed(src="/map.html", style=me.Style(width="100%", height="100%"),)

          except Exception as e:
              error_message = f"An error occurred: {str(e)}"
              me.text(error_message)
              raise