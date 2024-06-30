import streamlit as st
from requests.exceptions import ChunkedEncodingError
from streamlit_float import *
import pandas as pd
import plotly.express as px
import fungsiumum as fu
import fungsipeta as fp
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation

st.set_page_config(
    page_title="Database Outlet",
    page_icon="fishtail.png",
    layout="wide",
    menu_items={"About": """##### Database Outlet Juni 2024. 
            Author: Database Outlet
Email: databaseoutlet@gmail.com
            """}
)


def on_click():
    st.session_state.awal =" "

def on_clear():
    st.session_state.bersih=False


# Initialize session state variables if they don't exist
if "awal" not in st.session_state:
    st.session_state.awal = ""
if "tujuan" not in st.session_state:
    st.session_state.tujuan = ""

if st.checkbox("Tentukan Lokasi Anda", key="bersih"):
    loc = get_geolocation()

    if loc:
        latitude = loc['coords']['latitude']
        longitude = loc['coords']['longitude']

        st.caption(f"Koordinat Lokasi Anda, Lat: " + str(latitude) + ", Lon: " + str(longitude))

        tab1, tab2 = st.tabs(["Peta Outlet", "Peta Cluster Outlet"])
        with tab1:
            # Show the map
            fig = fp.addmap(latitude, longitude, 13, "maps/output.parquet")
            event = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

            st.caption("Hitung Jarak:")
            try:
                lat = event.selection["points"][0]["lat"]
                lon = event.selection["points"][0]["lon"]

                coordinates = f"{lat}, {lon}"

                if st.session_state.awal == " ":
                    st.session_state.awal = ""
                    st.session_state.tujuan = ""
                elif st.session_state.awal == "" and st.session_state.tujuan == "":
                    # If both are empty, set the initial coordinates to awal
                    st.session_state.awal = coordinates
                elif st.session_state.awal != "" and st.session_state.tujuan == "":
                    # If awal is filled, set the coordinates to tujuan
                    st.session_state.tujuan = coordinates

                colc1, colc2, colc3, colc4 = st.columns([1.1, 1.1, 2, 2])
                with colc1:
                    coordinate1 = st.text_input("Koordinat Awal", key="awal")
                with colc2:
                    coordinate2 = st.text_input("Koordinat Tujuan", key="tujuan")

                if coordinate1 == "":
                    copy_to_clipboard(coordinates, coordinates, coordinates)
                elif coordinate2 == "":
                    copy_to_clipboard(coordinates, coordinates, coordinates)
                if coordinate1 != "" and coordinate2 != "":
                    colb1, colb2, colb3, colb4, colb5, colb6 = st.columns([1, 1, 1, 1, 1, 1])
                    with colb1:
                        if st.button("Hitung Jarak", use_container_width=True):
                            try:
                                lat1, lon1 = map(float, coordinate1.split(','))
                                lat2, lon2 = map(float, coordinate2.split(','))
                                distance = fu.addDistance(lat1, lon1, lat2, lon2)
                                st.caption(f"{distance[0]}")
                            except ValueError:
                                st.caption("Invalid input format. Please enter coordinates as 'lat, lon'.")
                    with colb2:
                        if st.button("Hitung G-Maps", use_container_width=True):
                            try:
                                lat1, lon1 = map(float, coordinate1.split(','))
                                lat2, lon2 = map(float, coordinate2.split(','))
                                distance = fu.addDistancegmaps(lat1, lon1, lat2, lon2)
                                st.caption(distance)
                            except ValueError:
                                st.caption("Invalid input format. Please enter coordinates as 'lat, lon'.")
                    with colb3:
                        try:
                            st.link_button("Google Maps",
                                           "https://www.google.com/maps/dir/?api=1&origin=" + coordinate1 + ""
                                            "&destination=" + coordinate2 + "&travelmode=driving",
                                           use_container_width=True)
                        except ValueError:
                            st.link_button("Google Maps",
                                           "https://www.google.com/maps/dir/?api=1&origin="
                                           "&destination=&travelmode=driving",
                                           use_container_width=True)
                    with colb4:
                        if st.button("Hitung OSM",use_container_width=True):
                            lat1, lon1 = map(float, coordinate1.split(','))
                            lat2, lon2 = map(float, coordinate2.split(','))
                            distance = fu.addDistance(lat1, lon1, lat2, lon2)
                            if distance[1] <= 3:
                                try:
                                    distance = fu.addDistanceosm(lat1, lon1, lat2, lon2)
                                    st.caption(distance[0])
                                    st.write_stream(distance[1])
                                except ChunkedEncodingError:
                                    st.caption("Server commnunication error, please try again")
                                except (ValueError):
                                    st.caption("Invalid input format. Please enter coordinates as 'lat, lon'.")
                            else:
                                try:
                                    st.caption("Jarak " + str(
                                        f"{distance[1]:.2f}") + " km. *** Untuk akurasi Hitung OSM, jarak maksimal 3 km ***")
                                except (ValueError):
                                    st.caption("Invalid input format. Please enter coordinates as 'lat, lon'.")

                    with colb5:
                        st.button("Bersihkan Koordinat", on_click=on_click, use_container_width=True)
                    with colb6:
                        st.button("Bersihkan Peta", on_click=on_clear, use_container_width=True)
            except (KeyError, IndexError):
                st.caption("Koordinat belum dipilih, click titik koordinat outlet di peta")

        with tab2:

            cluster = st.radio("Pilih Cluster",["Cluster Branch", "Cluster Kab/Kota"],index=None)
            if cluster == "Cluster Branch":
                fig = fp.addmapcluster(latitude, longitude, 2, "maps/output.parquet")
                st.plotly_chart(fig, use_container_width=True)
            if cluster == "Cluster Kab/Kota":
                fig = fp.addmapkotakab(latitude, longitude, 2, "maps/output.parquet")
                st.plotly_chart(fig, use_container_width=True)