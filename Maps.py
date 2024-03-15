import folium
import streamlit as st
import geopandas as gpd
import pydeck as pdk
from streamlit_float import *
import altair as alt
import pandas as pd
import plotly.express as px
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium
import fungsi as fu

st.set_page_config(
    page_title = "Hotspot Kebakaran Lahan Hutan dan Polusi Udara",
    page_icon="fishtail.png",
    layout="wide",
    menu_items={"About":"""##### Pengaruh Hotspot Di Musim El Nino Oktober 2023 Terhadap Generasi Masa Depan. 
            Author: Jeffri Argon
Email: jeffriargon@gmail.com
            """}
)
float_init()


urlbubble = "https://github.com/thedo32/hotspotplb/blob/master/data/idn.topojson"




left_cl, main_cl= st.columns([1,8])
with left_cl:
     containup = st.container()
     containup.float()
     containup.markdown("[↗️⬆️↖️](#pendahuluan)", unsafe_allow_html=True)
     with st.container(border=True):
        st.markdown("<h5 style='text-align: left; color: #0B60B0;'>Section:</h5>", unsafe_allow_html=True)
        st.markdown("""
        - [Peta](#peta-sebaran-hotspot-kebakaran-hutan-lahan-bulan-oktober-2023)
        - [Diagram](#diagram-tingkat-ispu-pada-bulan-oktober-2023)
        - [Korrelasi](#korrelasi)
        - [Insight](#insight)
        """, unsafe_allow_html=True)
     st.markdown("<br>", unsafe_allow_html=True)
     with st.container(border=True):
        # st.image("img/free_palestine.png")
        st.markdown("<br>", unsafe_allow_html=True)
        st.image("img/from_river.png")
     st.markdown("<br>", unsafe_allow_html=True)
     with st.container(border=True):
        st.markdown("<p style='text-align: left; color: #0B60B0;'>By: Jeffri Argon</p>", unsafe_allow_html=True)

with (main_cl):

        st.subheader('Peta Sebaran Hotspot Kebakaran Hutan Lahan Bulan Oktober 2023')

        #tab untuk peta 3 wilayah administrasi
        tab1a, tab1b, tab1c, tab1d= st.tabs(['Indonesia Bubble','Indonesia Pyplot','Indonesia Altair', 'Indonesia Folium'])
        with tab1a:
            df = pd.read_csv('maps/idn_hs_by_prov.csv')
            # Create the choropleth bubble map
            fig = px.scatter_mapbox(
                df,
                lat="latitude",
                lon="longitude",
                size="count",  # Bubble size based on the "count" attribute
                mapbox_style="carto-darkmatter",  # Choose a suitable projection
                labels={"count": "Jumlah Hotspot"},
                hover_name="prov",  # Display count on hover
                color_discrete_sequence=["#5BA3CF"],  # Customize bubble color
                height=600,
                zoom=3.7,
                center=dict(lat=-3.1940, lon=117.5540),  # this will center on the point
            )

            # Show the map
            st.plotly_chart(fig, use_container_width=True)
            # st.markdown("Sumber Data Peta: [Geojson](%s)" % urlbubble, unsafe_allow_html=True)

        with tab1b:

            values = st.select_slider(
                'Pilih Wilayah Administrasi Pyplot', options=["Kota Palembang","Provinsi Sumsel","Indonesia"])
            if values == "Kota Palembang":
                df = pd.read_csv('maps/palembang75.csv')

                # Create the choropleth bubble map
                fig = px.scatter_mapbox(
                    df,
                    lat="Latitude",
                    lon="Longitude",
                    size="Jumlah",  # Bubble size based on the "count" attribute
                    mapbox_style="carto-darkmatter",  # Choose a suitable projection
                    labels={"Jumlah": "Jumlah (Total di Bubble Besar x100)"},
                    # hover_name="prov",  # Display count on hover
                    color_discrete_sequence=["#5BA3CF"],  # Customize bubble color
                    height=600,
                    zoom=8,
                    center=dict(lat=-2.9831,lon=104.7527),  # this will center on the point
                )

                # Show the map
                st.plotly_chart(fig, use_container_width=True)

            if values == "Provinsi Sumsel":
                df = pd.read_csv('maps/sumsel.csv')
                # Create the choropleth bubble map
                fig = px.scatter_mapbox(
                    df,
                    lat="Latitude",
                    lon="Longitude",
                    size="Jumlah",  # Bubble size based on the "count" attribute
                    mapbox_style="carto-darkmatter",  # Choose a suitable projection
                    labels={"Jumlah": "Jumlah (Total di Bubble Besar x100)"},
                    # hover_name="prov",  # Display count on hover
                    color_discrete_sequence=["#5BA3CF"],  # Customize bubble color
                    height=600,
                    zoom=7,
                    center=dict(lat=-2.9357, lon=104.4177),  # this will center on the point
                )

                # Show the map
                st.plotly_chart(fig, use_container_width=True)

            if values == "Indonesia":
                df = pd.read_csv('maps/idn.csv')


                # Create the choropleth bubble map
                fig = px.scatter_mapbox(
                    df,
                    lat="Latitude",
                    lon="Longitude",
                    size="Jumlah",  # Bubble size based on the "count" attribute
                    mapbox_style="carto-darkmatter",  # Choose a suitable projection
                    labels={"Jumlah": "Jumlah (Total di Bubble Besar x100)"},
                    # hover_name="prov",  # Display count on hover
                    color_discrete_sequence=["#5BA3CF"],  # Customize bubble color
                    height=600,
                    zoom=3.7,
                    center=dict(lat=-3.1940, lon=117.5540),  # this will center on the point
                )

                # Show the map
                st.plotly_chart(fig, use_container_width=True)

        with tab1c:
            values = st.select_slider(
            'Pilih Wilayah Administrasi Altair',options=["Kota Palembang","Provinsi Sumsel","Indonesia"] )
            if values == "Kota Palembang":
                    df1 = gpd.read_file('maps/palembang75.min.topojson')

                    df1['lon'] = df1.geometry.x  # extract longitude from geometry
                    df1['lat'] = df1.geometry.y  # extract latitude from geometry
                    df1 = df1[['lon', 'lat']]  # only keep longitude and latitude

                    firms_pl = pd.DataFrame(
                        df1,
                        columns=['lat', 'lon'])

                    st.pydeck_chart(pdk.Deck(
                        map_provider='carto',
                        map_style='dark',
                        views=pdk.View(type="mapview", controller=True),
                        initial_view_state=pdk.ViewState(
                            latitude=-2.9831,
                            longitude=104.7527,
                            zoom=8,
                        ),
                        layers=[
                            pdk.Layer(
                                'ScatterplotLayer',
                                data=firms_pl,
                                get_position='[lon, lat]',
                                get_color='[91, 163, 207, 200]',
                                get_radius=300,
                            ),
                        ],
                    ))

            if values == "Provinsi Sumsel":
                    df1 = gpd.read_file('maps/sumsel.min.topojson')

                    df1['lon'] = df1.geometry.x  # extract longitude from geometry
                    df1['lat'] = df1.geometry.y  # extract latitude from geometry
                    df1 = df1[['lon', 'lat']]  # only keep longitude and latitude

                    firms_pl = pd.DataFrame(
                        df1,
                        columns=['lat', 'lon'])

                    st.pydeck_chart(pdk.Deck(
                        map_provider='carto',
                        map_style='dark',
                        views=pdk.View(type="mapview", controller=True),
                        initial_view_state=pdk.ViewState(
                            latitude=-2.9357,
                            longitude=104.4177,
                            zoom=7,
                        ),
                        layers=[
                            pdk.Layer(
                                'ScatterplotLayer',
                                data=firms_pl,
                                get_position='[lon, lat]',
                                get_color='[91, 163, 207, 200]',
                                get_radius=300,
                            ),
                        ],
                    ))

            if values == "Indonesia":
                    df1 = gpd.read_file('maps/idns.min.topojson')

                    df1['lon'] = df1.geometry.x  # extract longitude from geometry
                    df1['lat'] = df1.geometry.y  # extract latitude from geometry
                    df1 = df1[['lon', 'lat']]  # only keep longitude and latitude

                    firms_pl = pd.DataFrame(
                        df1,
                        columns=['lat', 'lon'])

                    st.pydeck_chart(pdk.Deck(
                        map_provider='carto',
                        map_style='dark',
                        views=pdk.View(type="mapview", controller=True),
                        initial_view_state=pdk.ViewState(
                            latitude=-3.1940,
                            longitude=117.5540,
                            zoom=3.7,
                        ),
                        layers=[
                            pdk.Layer(
                                'ScatterplotLayer',
                                data=firms_pl,
                                get_position='[lon, lat]',
                                get_color='[91, 163, 207, 200]',
                             get_radius=300,
                            ),
                        ],
                    ))


        with tab1d:
            #set callback
            callback = """\
            function (row) {
                    var icon, marker;
                    icon = L.AwesomeMarkers.icon({
                        icon: "fire", iconColor: "#86BCDC", iconSize: [5,5]});
                    marker = L.marker(new L.LatLng(row[0], row[1]) );
                    marker.setIcon(icon);
                    return marker;
            };
            """

            # draw map
            m = folium.Map(location=[-3.1940, 117.5540],
                               tiles = 'cartodbdarkmatter',
                               zoom_start=2,
                               control_scale=True)


            if st.checkbox("Tampilkan Hotspot", value=False):
                values = st.select_slider(
                    'Pilih Wilayah Administrasi Folium', options=["Kota Palembang","Provinsi Sumsel","Indonesia"])
                if values == "Kota Palembang":
                    # draw map
                    m = folium.Map(location=[-2.9831,104.7527],
                                   tiles='cartodbdarkmatter',
                                   zoom_start=9,
                                   control_scale=True)
                    # Add marker cluster to map
                    points = gpd.read_file('maps/palembang75.min.topojson')
                if values == "Provinsi Sumsel":
                    m = folium.Map(location=[-2.9357, 104.4177],
                                   tiles='cartodbdarkmatter',
                                   zoom_start=9,
                                   control_scale=True)
                    points = gpd.read_file('maps/sumsel.min.topojson')
                if values == "Indonesia":
                    poinst = gpd.read_file('maps/idns.min.topojson')


                # Get x and y coordinates for each point
                # points_gjson = folium.features.GeoJson(points, name="Hotspot Indonesia")
                # points_gjson.add_to(m)

                # Get x and y coordinates for each point
                points["x"] = points["geometry"].x
                points["y"] = points["geometry"].y

                # Create a list of coordinate pairs
                locations = list(zip(points["y"], points["x"]))

                # Create a folium marker cluster
                fast_marker_cluster = FastMarkerCluster(locations, callback=callback, control=True)

                fast_marker_cluster.add_to(m)


            # draw maps
            st_folium(m,height=450, use_container_width=True)





        with st.expander("Analisis Peta"):
            st.markdown("Dapat dilihat :blue[disekitar Kota Palembang terdapat banyak hotspot],"
                     "juga kalau kita melihat ke wilayah Provinsi Sumatera Selatan, sebaran hotspot terdapat lebih banyak di "
                     ":blue[bagian tenggara provinsi dan tidak jauh dari ibu kota provinsi tersebut]. "
                     "Jika keseluruhan di peta Indonesia terdapat kecerahan hostpot hampir mirip di beberapa wilayah, "
                     "kemudian jika melihat peta Indonesia Bubble "
                     "di Sumatera Selatan terdapat 15.848 hotspot, :blue[terbanyak dibandingkan provinsi lain], "
                     "dan dibawahnya Kalimantan Tengah sebanyak 13.393 hotspot, dari total 78.759 hoitspot di Indonesia.<br><br>", unsafe_allow_html=True)
        
        



