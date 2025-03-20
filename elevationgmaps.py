import requests

def get_elevation_google(lat, lon, api_key):
    url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lon}&key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            elevation = data["results"][0]["elevation"]
            return elevation
        else:
            return "No elevation data found."
    else:
        return "API request failed."


# Example Usage:
API_KEY = 'xxxxxx'  # Replace with your Google API key



# Example Us
latitude = -0.393537948426002  # Replace with your latitude
longitude = 100.4571598213546  # Replace with your longitude

elevation = get_elevation_google(latitude, longitude, API_KEY)
print(f"Elevation at ({latitude}, {longitude}): {elevation} meters")
