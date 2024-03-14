import pandas as pd
import geopy.distance


def addDistance (inputPath,outputPath) :
    dfirms = pd.read_csv(inputPath)


    coords_1 = [dfirms["latitude"], dfirms["longitude"]]
    coords_2 = [dfirms["lat_pol"], dfirms["lon_pol"]]


    for i in range(len(dfirms)):
        coords_1 = (dfirms.loc[i, "latitude"], dfirms.loc[i, "longitude"])
        coords_2 = (dfirms.loc[i, "lat_pol"], dfirms.loc[i, "lon_pol"])
        distance = geopy.distance.geodesic(coords_1, coords_2).km
        print(distance)
        df = pd.DataFrame({distance})
        df.to_csv(outputPath, mode="a", index=False, header=False)