import pykml as kml
import codecs
import pandas as pd
from pykml import parser


# Membaca file KML
with codecs.open('test_input.kml', 'r', encoding="utf-8", errors='ignore') as f:
    root = parser.parse(f).getroot()

places = []
for place in root.Document.Folder.Placemark:
    data = {item.get("name"): item.text for item in
            place.ExtendedData.SchemaData.SimpleData}
    coords = place.Polygon.outerBoundaryIs.LinearRing.coordinates.text.strip().split(' ')
    data["Coordinates"] = coords
    places.append(data)
df = pd.DataFrame(places)
print(df)