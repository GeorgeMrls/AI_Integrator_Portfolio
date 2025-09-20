import requests
import json
from pathlib import Path
import argparse
import logging
import csv

# Base
BASE_URL = "https://api.open-meteo.com/v1/forecast"

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch Open-Meteo forecast and save JSON")
    parser.add_argument("--lat", type=float, default=37.98, help= "latitude (default: 37.98)")
    parser.add_argument("--lon", type=float, default=23.72, help= "longitude (default: 23.72)" )
    parser.add_argument(
        "--out",
        type= Path,
        default= Path(__file__).parent / "data" / "athens_weather.json",
        help="Output JSON path"
    )
    parser.add_argument("--hours", type=int, help="limit forecast to N hours ahead")
    parser.add_argument("--verbose", action="store_true", help="Enable detailed logs")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format (default: json)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    #---logging setup---
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    logging.debug(f"Args:{args}")



    PARAMS = {
        "latitude": args.lat,
        "longitude": args.lon,
        "hourly": "temperature_2m"
    }
    logging.info("Fetching data from %s ...", BASE_URL)
    resp = requests.get(BASE_URL, params=PARAMS, timeout=(5, 20))
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
   
if args.format == "json":
    # JSON save
    with output_f.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logging.info("Saved JSON to %s", output_f)

else:  # CSV
    if output_f.suffix.lower() != ".csv":
        output_f = output_f.with_suffix(".csv")

    try:
        times = data["hourly"]["time"]
        temps = data["hourly"]["temperature_2m"]
    except KeyError:
        logging.error("Hourly payload missing 'time' or 'temperature_2m'; cannot write CSV")
        raise SystemExit(1)

    with output_f.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "temperature_2m"])
        writer.writerows(zip(times, temps))

    logging.info("Saved CSV to %s", output_f)