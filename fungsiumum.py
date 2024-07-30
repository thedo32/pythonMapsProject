import pandas as pd
import geopy.distance
import csv
import geojson
import streamlit as st
import networkx as nx
import osmnx as ox
import taxicab as tc
import googlemaps
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


@st.cache_resource
def addDistances(inputPath, outputPath):
    dfloc = pd.read_csv(inputPath)

    for i in range(len(dfloc)):
        coords_1 = (dfloc.loc[i, "latitude"], dfloc.loc[i, "longitude"])
        coords_2 = (dfloc.loc[i, "lat_pol"], dfloc.loc[i, "lon_pol"])
        distance = geopy.distance.geodesic(coords_1, coords_2).km
        print(distance)
        df = pd.DataFrame({distance})
        df.to_csv(outputPath, mode="a", index=False, header=False)


def addDistance(lat1, lon1, lat2, lon2):
    # Calculating the distance
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    intDistance = geopy.distance.geodesic(coords_1, coords_2).km
    addedDistance = (f"Jarak: {intDistance:.2f} km")
    return addedDistance, intDistance


def addDistanceosm(lat1, lon1, lat2, lon2):
    G = ox.graph_from_point([lat1, lon1], 3000, dist_type="network",
                            network_type="drive")
    awal = ox.nearest_nodes(G, lon1, lat1)
    tujuan = ox.nearest_nodes(G, lon2, lat2)
    distance = nx.shortest_path_length(G, awal, tujuan, weight="length") / 1000
    addedDistanceosm = (f"Jarak: {distance:.2f} km")
    awaltc = (lat1, lon1)
    tujuantc = (lat2, lon2)
    tcdistance = tc.shortest_path(G, awaltc, tujuantc)
    tcDistanceosm = tc.plot_graph_route(G, tcdistance, route_linewidth=4)
    return addedDistanceosm, tcDistanceosm


def addDistancegmaps(lat1, lon1, lat2, lon2):
    # Requires API key
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    distance = gmaps.distance_matrix([[lat1, lon1]], [[lat2, lon2]], mode="driving")['rows'][0]['elements'][0]
    addedDistance = distance["distance"]["text"]
    return addedDistance


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
    if wilayah == "Brand Outlets Branch":
        return pd.read_csv('maps/dataoutletskabclips.csv'), [
            {"text": "2142", "lat": -3.47, "lon": 105.96, "radius": 6000}], 8, 0.5072459760797242, 101.44711771077857
    elif wilayah == "Brand Outlets Subdist":
        return pd.read_csv('maps/dataoutletskabclips.csv'), [
            {"text": "15848", "lat": -3.47, "lon": 106.139, "radius": 12000}], 7, 0.5072459760797242, 101.44711771077857
    elif wilayah == "Indonesia":
        return pd.read_csv('maps/dataoutletskabclips.csv'), [
            {"text": "6194", "lat": -4, "lon": 117.5, "radius": 85000}], 3.7, -4, 117.5
