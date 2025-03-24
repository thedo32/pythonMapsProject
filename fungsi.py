import pandas as pd
import geopy.distance
import csv
import os
import json
import geojson
import streamlit as st
import googlemaps
from datetime import datetime, timedelta
from dotenv import load_dotenv

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time

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


# Function to load dataset based on wilayah selection
def wilayah_admin_geo(wilayah):
    if wilayah == "Kota Palembang":
        return pd.read_csv('maps/palembang50.csv'), 8, -2.9831, 104.7527
    elif wilayah == "Provinsi Sumsel":
        return pd.read_csv('maps/sumsel.csv'), 7, -2.9357, 104.4177
    elif wilayah == "Indonesia":
        return pd.read_csv('maps/idn.csv'), 3.7, -4, 117.5
    return None, None, None, None

def wilayah_admin(wilayah):
    if wilayah == "Kota Palembang":
        return pd.read_csv('maps/palembang50.csv'), [{"text": "2142", "lat": -3.47, "lon": 105.96, "radius": 6000}], 8, -2.9831, 104.7527
    elif wilayah == "Provinsi Sumsel":
        return pd.read_csv('maps/sumsel.csv'), [{"text": "15848", "lat": -3.47, "lon": 106.139, "radius": 12000}],7, -2.9357, 104.4177
    elif wilayah == "Indonesia":
        return pd.read_csv('maps/idn.csv'), [{"text": "6194", "lat": -4, "lon": 117.5, "radius": 85000}], 3.7, -4, 117.5


# Function to get location using Google Maps API
def get_location(lat, lon,wilayah):

    load_dotenv()
    API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Replace with your actual Google API Key
    gmaps = googlemaps.Client(key=API_KEY)

    if wilayah == "Kota Palembang":
        # File to cache geolocation results
        cache_file = "location_cache_3.json"
    elif wilayah == "Provinsi Sumsel":
        # File to cache geolocation results
        cache_file = "location_cache_2.json"
    elif wilayah == "Indonesia":
        # File to cache geolocation results
        cache_file = "location_cache_1.json"

    max_age_days = 90  # 3 months

    # Check if cache file is recent
    def is_cache_valid():
        if not os.path.exists(cache_file):
            return False  # No cache file found

        file_mod_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        if file_mod_time < datetime.now() - timedelta(days=max_age_days):
            return False  # File is too old

        return True  # Cache is valid

    # Load cached locations if file is still valid
    if is_cache_valid():
        with open(cache_file, "r") as f:
            location_cache = json.load(f)
    else:
        print("⚠️ Cache file is too old or missing, fetching new data...")
        location_cache = {}

    key = f"{lat},{lon}"

    if key in location_cache:
        return location_cache[key]  # Return cached result

    try:
        result = gmaps.reverse_geocode((lat, lon))
        address = result[0]["formatted_address"] if result else "Unknown Location"

        # Save new location to cache
        location_cache[key] = address

        # Save cache to file
        with open(cache_file, "w") as f:
            json.dump(location_cache, f)

        return address
    except Exception as e:
        print(f"Google Geocoding Error: {e}")
        return "Unknown Location"




