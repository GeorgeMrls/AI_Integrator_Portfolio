import requests
import json
from pathlib import Path
import argparse
import logging
import csv

# Base
BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

def resolve_city_to_coords(city, country=None):
    """Call Open-Meteo geocoding API and return (lat, lon)."""
    params = {"name": city}
    if country:
        params["country"] = country

    resp = requests.get("https://geocoding-api.open-meteo.com/v1/search", params=params, timeout=10)
    resp.raise_for_status()
    results = resp.json().get("results")
    if not results:
        raise ValueError(f"No geocoding results for {city}, {country or ''}")
    
    # Παίρνουμε το πρώτο αποτέλεσμα
    best = results[0]
    return best["latitude"], best["longitude"]


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch Open-Meteo forecast and save JSON")
    
    parser.add_argument(
    "--city",
    type=str,
    required=True,
    help="City name (e.g., Athens)"
    )

    parser.add_argument(
    "--country",
    type=str,
    required=True,
    help="Country code, ISO-2 (e.g., GR for Greece, US for USA)"
    )

    parser.add_argument(
        "--out",
        type= Path,
        default= Path(__file__).parent / "data" / "athens_weather.json",
        help="Output JSON path"
    )
    parser.add_argument("--hours", type=int, help="limit forecast to N hours ahead")
    parser.add_argument("--verbose", action="store_true", help="Enable detailed logs")
    parser.add_argument("--format", choices=["json", "csv", "both"], default="json", help="Output format json, csv or both (default: json)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    # Normalize country to uppercase
    if args.country:
        args.country = args.country.upper()

    #---logging setup---
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    logging.debug(f"Args:{args}")

    # -- geocoding --
    try:
        lat, lon = resolve_city_to_coords(args.city, args.country)
        logging.info("Resolved %s, %s -> lat=%.2f, lon=%.2f", args.city, args.country, lat, lon)
    except ValueError as e:
        logging.error(str(e))
        raise SystemExit(1)


    PARAMS = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m"
    }
    logging.info("Fetching data from %s ...", BASE_URL)
    resp = requests.get(BASE_URL, params=PARAMS, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if args.hours:
        try:
            data["hourly"]["time"] = data["hourly"]["time"][:args.hours]
            data["hourly"]["temperature_2m"] = data["hourly"]["temperature_2m"][:args.hours]
        except KeyError:
            logging.warning("Unexpected hourly payload; cannot slice hours")


    output_f = args.out
    output_f.parent.mkdir(parents=True, exist_ok=True)

# --- JSON save ---
    if args.format in ["json", "both"]:
        out_json = output_f.with_suffix(".json")
        with out_json.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logging.info("Saved JSON to %s", out_json)

# --- CSV save ---
    if args.format in ["csv", "both"]:
        out_csv = output_f.with_suffix(".csv")
        try:
            times = data["hourly"]["time"]
            temps = data["hourly"]["temperature_2m"]
        except KeyError:
            logging.error("Hourly payload missing 'time' or 'temperature_2m' ; cannot write CSV")
            raise SystemExit(1)
            
        with out_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["time", "temperature_2m"])
            writer.writerows(zip(times, temps))

        logging.info("Saved CSV to %s", out_csv)

    print("Data saved successfully.")