import requests
import json
from pathlib import Path
import argparse
import logging
import csv
import os
from openai import OpenAI
from datetime import date

# Base
BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch Open-Meteo forecast and save JSON")
    
    parser.add_argument("--city", type=str, required=True, help="City name (e.g., Athens)")
    parser.add_argument("--country", type=str, required=True, help="Country code, ISO-2 (e.g., GR for Greece, US for USA)")
    parser.add_argument("--out", type= Path, default= Path(__file__).parent / "data" / "athens_weather.json", help="Output JSON path")
    parser.add_argument("--hours", type=int, help="limit forecast to N hours ahead")
    parser.add_argument("--verbose", action="store_true", help="Enable detailed logs")
    parser.add_argument("--format", choices=["json", "csv", "both"], default="json", help="Output format json, csv or both (default: json)")
    parser.add_argument("--report", choices=["txt", "md", "llm"], help="Makes report (txt/md domestic, llm with OpenAI)")
    parser.add_argument("--model", default="gpt-4.1-mini", help="OpenAI model for LLM report")
    parser.add_argument("--date", type=str, help="Ημερομηνία YYYY-MM-DD (default: today)")
    
    return parser.parse_args()



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
    
    # Get Result
    best = results[0]
    return best["latitude"], best["longitude"]


def compute_stats(data: dict):
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    if not times or not temps:
        return None
    t_min = min(temps); i_min = temps.index(t_min)
    t_max = max(temps); i_max = temps.index(t_max)
    avg = sum(temps) / len(temps)
    return {"t_min": t_min, "t_max": t_max, "avg": avg,
            "t_min_time": times[i_min], "t_max_time": times[i_max], "n": len(temps)}


def generate_weather_report_llm(stats: dict, city: str, country: str, model: str = "gpt-4.1-mini") -> str:
    if not stats:
        return "No hourly data to summarize."
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Missing OPENAI_API_KEY env var.")
    client = OpenAI()  
    prompt = (
        f"Write a concise weather report (3-5 sentences) for {city}, {country} on {req_date}. "
        f"Minimum {stats['t_min']} at {stats['t_min_time']}, "
        f"Maximum {stats['t_max']} at {stats['t_max_time']}, "
        f"Mean {stats['avg']:.1f} across {stats['n']} hourly points. "
        "Neutral tone, no hype."
)
    resp = client.responses.create(model=model, input=prompt)
    return resp.output_text.strip()



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
    
    req_date = args.date or date.today().isoformat()
    PARAMS = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "start_date": req_date,
        "end_date": req_date,
        "timezone": "auto",
    }

    logging.info("Fetching data from %s ...", BASE_URL)
    resp = requests.get(BASE_URL, params=PARAMS, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    
    ''' You can use this to slice hours, unless it is given 24hrs
    if args.hours:
        try:
            data["hourly"]["time"] = data["hourly"]["time"][:args.hours]
            data["hourly"]["temperature_2m"] = data["hourly"]["temperature_2m"][:args.hours]
        except KeyError:
            logging.warning("Unexpected hourly payload; cannot slice hours") '''

    stats = compute_stats(data)

    if args.report == "llm":
      report_text = generate_weather_report_llm(stats, args.city, args.country, model=args.model)
      out_md = args.out.with_suffix(".md")
      out_md.write_text(report_text, encoding="utf-8")
      logging.info("Saved LLM report to %s", out_md)


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