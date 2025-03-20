import requests


def get_elevation(lat, lon):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    response = requests.get(url)

    if response.status_code == 200:
        elevation = response.json()['results'][0]['elevation']
        return elevation
    else:
        return None


# -0.39125982567462636, 100.45461577228333

# -0.39127615674304195, 100.45259211841844

# -0.3889230738717576, 100.46437448355528

# -0.3822707959334041, 100.46864146979847

# -0.39353099491389304, 100.45715834025985

# Example Us
latitude = -0.37841657   # Replace with your latitude
longitude = 100.46968505  # Replace with your longitude

elevation = get_elevation(latitude, longitude)

if elevation is not None:
    print(f"Elevation at ({latitude}, {longitude}): {elevation} meters")
else:
    print("Failed to retrieve elevation data")