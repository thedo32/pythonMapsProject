import pandas as pd
import geopy.distance
import csv
import geojson
import streamlit as st

@st.cache_resource

def addDistance (inputPath,outputPath) :
    dfloc = pd.read_csv(inputPath)

    for i in range(len(dfloc)):
        coords_1 = (dfloc.loc[i, "latitude"], dfloc.loc[i, "longitude"])
        coords_2 = (dfloc.loc[i, "lat_pol"], dfloc.loc[i, "lon_pol"])
        distance = geopy.distance.geodesic(coords_1, coords_2).km
        print(distance)
        df = pd.DataFrame({distance})
        df.to_csv(outputPath, mode="a", index=False, header=False)

def csv_to_geojson(csv_file, geojson_file):
    features = []
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            # Assuming your CSV has 'latitude' and 'longitude' columns
            latitude = float(row['latitude'])
            longitude = float(row['longitude'])

            feature = geojson.Feature(
                geometry=geojson.Point((longitude, latitude)),
                properties=row
            )
            features.append(feature)

    feature_collection = geojson.FeatureCollection(features)

    with open(geojson_file, 'w') as f:
        geojson.dump(feature_collection, f, indent=2)

def format_big_number(num):
    if num >= 1e6:
        return f"{num / 1e6:.1f} Mio"
    elif num >= 1e3:
        return f"{num / 1e3:.1f} K"
    elif num >= 1e2:
        return f"{num / 1e3:.1f} K"
    else:
        return f"{num:.2f}"

def wilayah_admin(wilayah):
    if wilayah == "Kota Palembang":
        return pd.read_csv('maps/palembang50.csv'), [{"text": "2142", "lat": -3.47, "lon": 105.96, "radius": 6000}], 8, -2.9831, 104.7527
    elif wilayah == "Provinsi Sumsel":
        return pd.read_csv('maps/sumsel.csv'), [{"text": "15848", "lat": -3.47, "lon": 106.139, "radius": 12000}],7, -2.9357, 104.4177
    elif wilayah == "Indonesia":
        return pd.read_csv('maps/idn.csv'), [{"text": "6194", "lat": -4, "lon": 117.5, "radius": 85000}], 3.7, -4, 117.5




