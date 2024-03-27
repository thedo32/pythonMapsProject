import streamlit as st
import altair as alt
from io import StringIO
import folium
from streamlit_float import *
import pandas as pd
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium





uploaded_file1 = st.file_uploader("Pilih tabular dataframe", key=123)
if uploaded_file1 is not None:
    # To read file as bytes:
    bytes_data = uploaded_file1.getvalue()
    #st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file1.getvalue().decode("utf-8"))
    #st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    #st.write(string_data)

    df0 = pd.read_csv(uploaded_file1)

    if st.checkbox('Tampilkan Diagram', value=False):
        bars = alt.Chart(df0).mark_bar(size=25).encode(
            y="Status:O",
            x=alt.X("count(Value):Q", title="Jumlah Hari"),
            color=alt.Color("max(Color):N", scale=None)
        ).properties(height=180, width=360).interactive()
        st.altair_chart(bars)

    if st.checkbox('Tampilkan Presentase', value=False):
        base = alt.Chart(df0).mark_arc(innerRadius=50, outerRadius=105).encode(
                alt.Color("Persentase:O").legend(None),
                alt.Theta("count(Value):Q", title="Jumlah Hari").stack(True),
                # color=alt.Color("max(Color)", scale=None)
        ).properties(height=290, width=290).interactive()

        text = base.mark_text(radius=138, size=11).encode(text="Status:N")
        st.markdown("<br>", unsafe_allow_html=True)
        st.altair_chart(base + text, use_container_width=False)

uploaded_file2 = st.file_uploader("Pilih spatial dataframe", key=345)
if uploaded_file2 is not None:
    # To read file as bytes:
    bytes_data = uploaded_file2.getvalue()
    #st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file2.getvalue().decode("utf-8"))
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
        points = pd.read_csv(uploaded_file2)

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


