import requests
import json
from pathlib import Path

# Σταθερές
BASE_URL = "https://api.open-meteo.com/v1/forecast"
LAT = 37.98
LON = 23.72
PARAMS = {
    "latitude": LAT,
    "longitude": LON,
    "hourly": "temperature_2m"
}

# Request
response = requests.get(BASE_URL, params=PARAMS)
response.raise_for_status()  # Σταματάει αν υπάρχει error
data = response.json()

# Αποθήκευση σε JSON
output_file = Path(__file__).parent / "data" / "athens_weather.json"
output_file.parent.mkdir(exist_ok=True)
with open(output_file, "w") as f:
    json.dump(data, f, indent=2)

print(f"Data saved to {output_file}")