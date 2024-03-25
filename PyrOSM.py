import streamlit as st
import pyrosm
from pyrosm import get_data
import csv
import pandas as pd
fp = get_data("turin")
#osm = pyrosm.OSM(fp)

osm = pyrosm.OSM(fp, bounding_box=[7.628503,45.106031,7.646098,45.113814])
turin_allianz = osm.get_network(network_type="walking")
print(turin_allianz)

df = pd.DataFrame(turin_allianz)

df.to_csv('data/turin_allianz.csv', index=False)


