import folium
import streamlit as st
import geopandas as gpd
import pydeck as pdk
from streamlit_float import *
import altair as alt
import numpy as np
import pandas as pd
import plotly.express as px
from folium.plugins import MarkerCluster
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium
import numpy as np
from geopy.geocoders import Nominatim

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



url = "https://ditppu.menlhk.go.id/portal/read/indeks-standar-pencemar-udara-ispu-sebagai-informasi-mutu-udara-ambien-di-indonesia"
urllhk = "https://www.menlhk.go.id/"
urlsipongi = "https://sipongi.menlhk.go.id/"
urlfirms = "https://firms.modaps.eosdis.nasa.gov/api/country/"
urlopenwea = "https://openweathermap.org/api/air-pollution"
urlbmkg = "https://dataonline.bmkg.go.id/akses_data"
urlboston = "https://www.bc.edu/bc-web/centers/schiller-institute/sites/masscleanair/articles/children.html"
urlhalodoc = "https://www.halodoc.com/artikel/perlu-tahu-ini-7-gangguan-kesehatan-yang-dipicu-partikel-polusi-pm2-5"
urlnafas = "https://nafas.co.id/article/Apakah-PM2-5-berbahaya-untuk-anak-anak"
urlotc = "https://otcdigest.id/kesehatan-anak/polusi-udara-tingkatkan-risiko-adhd-pada-anak-anak"
urlkompastv = "https://www.kompas.tv/regional/448420/akibat-karhutla-kabut-asap-di-palembang-makin-pekat"
urlsctv = "https://www.liputan6.com/photo/read/5415505/diselimuti-kabut-asap-palembang-berlakukan-sekolah-daring?page=1"
urlbnpb = "https://bnpb.go.id/berita/99-penyebab-kebakaran-hutan-dan-lahan-adalah-ulah-manusia"
urlbubble = "https://github.com/thedo32/hotspotplb/blob/master/data/idn.geojson"

st.subheader('Peta Sebaran Hotspot Kebakaran Hutan Lahan Bulan Oktober 2023')

left_cl, main_cl= st.columns([1,8])
with left_cl:
     # containup = st.container()
     # containup.float()
     # containup.markdown("[↗️⬆️↖️](#pendahuluan)", unsafe_allow_html=True)
     with st.container(border=True):
        # st.image("img/free_palestine.png")
        st.markdown("<br>", unsafe_allow_html=True)
        st.image("img/from_river.png")
     st.markdown("<br>", unsafe_allow_html=True)
     with st.container(border=True):
        st.markdown("<p style='text-align: left; color: #0B60B0;'>By: Jeffri Argon</p>", unsafe_allow_html=True)

with (main_cl):
    with st.container(border=True):
        st.caption("Menurut data [SIPONGI KLHK](%s)" % urlsipongi + " dan [FIRMS NASA](%s)" % urlfirms + " "
                                                                                                          "pada bulan Oktober 2023, di wilayah :blue[Propinsi Sumatera Selatan] yang mempunyai penduduk 8,6 juta jiwa (BPS 2022), "
                                                                                                          "dan mempunyai metropolitan yang berkembang yakni Patungraya Agung yang berpenduduk 2,6 juta jiwa (BPS 2020), "
                                                                                                          "khususnya :blue[Kota Palembang yang berpenduduk sekitar 1,7 juta jiwa] (BPS 2022), "
                                                                                                          "terdapat hotspot :blue[terbanyak] dari kejadian Bencana Kebakaran Hutan Lahan dibanding propinsi lain di Indonesia, yang diperparah oleh fenomena El Nino. <br>"
                                                                                                          "**Puncak El Nino:**<br> "                                                                                      ""
                                                                                                          "Pada kondisi normalnya musim penghujan di mulai bulan oktober, "
                                                                                                          "namun menurut data BMKG, :blue[Temperatur yang tinggi, Presipitasi sangat rendah] terjadi di bulan Oktober 2023. Juga Berdasarkan historikal Data Matrix Sipongi di mana "
                                                                                                          ":blue[sering terjadi puncak kebakaran hutan lahan di bulan oktober pada tahun terjadinya El Nino].<br> "
                                                                                                          "Kondisi tersebut mengakibatkan terpaparnya polusi kabut asap yang meengakibatkan :blue[risiko kesehatan tinggi terhadap masyarakat, "
                                                                                                          "terutama pada kelompok rentan seperti anak-anak dan ibu hamil] yang dapat mengancam :blue[Generasi Masa Depan]",
                    unsafe_allow_html=True)

        #tab untuk peta 3 wilayah administrasi
        tab1a, tab1b, tab1c, tab1d, tab1e = st.tabs(['Indonesia Bubble','Pyplot','Altair Pydeck', 'Folium', "Folium with Popup"])
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
            col1, col2 = st.columns([1,1])
            with col1:
                values = st.select_slider(
                    'Pilih Wilayah Administrasi Pyplot', options=["Kota Palembang","Provinsi Sumsel","Indonesia"])

            # Get dataset
            df, zoom, center_lat, center_lon = fu.wilayah_admin_geo(values)

            if df is not None:
                # Add geolocation information
                df["Location"] = df.apply(lambda row: fu.get_location(row["Latitude"], row["Longitude"],values), axis=1)

                # Create the choropleth bubble map
                fig = px.scatter_mapbox(
                    df,
                    lat="Latitude",
                    lon="Longitude",
                    size="Jumlah",
                    mapbox_style="carto-darkmatter",
                    labels={"Jumlah": "Jumlah (Total di Bubble Besar x100)"},
                    hover_name="Location",  # Display geolocation in hover
                    hover_data={"Latitude": True, "Longitude": True, "Jumlah": True},  # Show additional info
                    color_discrete_sequence=["#5BA3CF"],
                    height=600,
                    zoom=zoom,
                    center=dict(lat=center_lat, lon=center_lon),
                )

                # Show the map
                st.plotly_chart(fig, use_container_width=True)



        with tab1c:
            col1, col2 = st.columns([1,1])
            with col1:
                values = st.select_slider(
                    'Pilih Wilayah Administrasi Altair', options=["Kota Palembang", "Provinsi Sumsel", "Indonesia"])

                # df1 = gpd.read_file('maps/palembang50.min.topojson')

                # df1['lon'] = df1.geometry.x  # extract longitude from geometry
                # df1['lat'] = df1.geometry.y  # extract latitude from geometry
                # df1 = df1[['lon', 'lat']]  # only keep longitude and latitude

                # firms_pl = pd.DataFrame(
                #     df1,
                #     columns=['lat', 'lon'])

            firms_pl = fu.wilayah_admin(values)
            #bubbletext = [{"text":"2142","lat":-3.47,"lon":105.96}]


            st.pydeck_chart(pdk.Deck(
                        map_provider='carto',
                        map_style='dark',
                        views=pdk.View(type="mapview", controller=True),
                        initial_view_state=pdk.ViewState(
                            latitude=firms_pl[3],
                            longitude=firms_pl[4],
                            zoom=firms_pl[2],
                        ),
                        layers=[
                            pdk.Layer(
                                'ScatterplotLayer',
                                data=firms_pl[0],
                                get_position='[Longitude, Latitude]',
                                get_color='[91, 163, 207, 200]',
                                get_radius=300,
                                pickable=True,
                            ),
                            pdk.Layer(
                                'ScatterplotLayer',
                                data=firms_pl[1],
                                get_position='[lon, lat]',
                                get_color='[91, 163, 207, 200]',
                                get_radius='[radius]',
                            ),
                            pdk.Layer(
                                'TextLayer',
                                data=firms_pl[1],
                                get_position='[lon, lat]',
                                gettext='[text]',
                                getSize=12,
                            ),
                        ],
                    )
            )



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

            m = folium.Map(location=[-3.1940, 117.5540],

                           tiles='http://{s}.api.tomtom.com/map/1/tile/sat/main/{z}/{x}/{y}.jpg?'
                                 'view=Unified&key=1s6goFp1aKAsD6yevSYzur1dPu67E8Qh',
                           attr='TomTom',
                           zoom_start=3,
                           control_scale=True)

            folium.raster_layers.TileLayer(
                tiles='http://{s}.api.tomtom.com/map/1/tile/labels/night/{z}/{x}/{y}.png?'
                      'view=Unified&key=1s6goFp1aKAsD6yevSYzur1dPu67E8Qh',
                attr='TomTom',
            ).add_to(m)



            if st.checkbox("Tampilkan Hotspot", value=False):
                col1, col2 = st.columns([1, 1])
                with col1:
                    values = st.select_slider(
                        'Pilih Wilayah Administrasi Folium', options=["Palembang", "SumselProv", "Indonesia"])

                points = pd.read_csv("maps/"+values+".csv")

                # Extract latitude and longitude columns
                locations = list(zip(points["Latitude"], points["Longitude"]))

                # Create a folium marker cluster
                fast_marker_cluster = FastMarkerCluster(locations, callback=callback, control=True)
                fast_marker_cluster.add_to(m)

                # draw maps

            image = np.zeros((61, 61))
            image[0, :] = 1.0
            image[60, :] = 1.0
            image[:, 0] = 1.0
            image[:, 60] = 1.0

            folium.raster_layers.ImageOverlay(
                image=image,
                bounds=[[0, -60], [60, 60]],
                colormap=lambda x: (1, 0, 0, x),
            ).add_to(m)



            st_folium(m, height=450, use_container_width=True,key=123)


        with tab1e:
            # draw basemap

            m = folium.Map(location=[-3.1940, 117.5540],

                           tiles='http://{s}.api.tomtom.com/map/1/tile/sat/main/{z}/{x}/{y}.jpg?'
                                 'view=Unified&key=1s6goFp1aKAsD6yevSYzur1dPu67E8Qh',
                           attr='TomTom',
                           zoom_start=2,
                           control_scale=True)

            folium.raster_layers.TileLayer(
                tiles='http://{s}.api.tomtom.com/map/1/tile/labels/night/{z}/{x}/{y}.png?'
                      'view=Unified&key=1s6goFp1aKAsD6yevSYzur1dPu67E8Qh',
                attr='TomTom',
            ).add_to(m)

            if st.checkbox("Tampilkan Hotspot? Don't bother, make or order your coffee while loading", value=False, disabled=False):
                col1, col2 = st.columns([1, 1])
                with col1:
                    values = st.select_slider(
                        'Pilih Wilayah Administrasi Folium Popup', options=["Palembang", "SumselProv", "Indonesia"])

                points = pd.read_csv("maps/" + values + ".csv")

                # Get x and y coordinates for each point
                # points_gjson = folium.features.GeoJson(points, name="Hotspot Indonesia")
                # points_gjson.add_to(m)
                # Get x and y coordinates for each point
                #points = pd.read_csv('maps/idns.csv')

                # Extract latitude and longitude columns
                marker_cluster = MarkerCluster(callback=callback)
                for _, row in points.iterrows():
                    popup = f"Latitude: {row['Latitude']}<br>Longitude: {row['Longitude']}"
                    folium.Marker([row['Latitude'], row['Longitude']], popup=popup).add_to(marker_cluster)

                marker_cluster.add_to(m)

            # Add maps to streamlit
            st_folium(m, height=450, use_container_width=True)


        with st.expander("Analisis Peta"):
            st.markdown("Tampilan peta ini menggunakan tiga library yang berbeda, yaitu Pyplot yang loadingnya cepat, namun tampilan petanya kurang atraktif dan kurang interaktif "
                        "kemudian Altair Pydeck yang performanya menengah, kemudian yang paling lama loadingnya tapi paling interaktif adalah Folium. "
                        "Sebagai informasi terkait, data Pyplot menggunakan format csv, lalau format topojson untuk Altair Pydeck dan Folium. "
                        "Untuk sebaran hotspot dapat dilihat :blue[disekitar Kota Palembang terdapat cukup banyak hotspot],"
                     "juga kalau kita melihat ke wilayah Provinsi Sumatera Selatan, sebaran hotspot terdapat lebih banyak di "
                     ":blue[bagian tenggara provinsi dan tidak jauh dari ibu kota provinsi tersebut]. "
                     "Jika keseluruhan di peta Indonesia terdapat kecerahan hostpot hampir mirip di beberapa wilayah, "
                     "kemudian jika melihat peta Indonesia Bubble "
                     "di Sumatera Selatan terdapat 15.848 hotspot, :blue[terbanyak dibandingkan provinsi lain], "
                     "dan dibawahnya Kalimantan Tengah sebanyak 13.393 hotspot, dari total 78.759 hoitspot di Indonesia.<br><br>", unsafe_allow_html=True)
        
        



