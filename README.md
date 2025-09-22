

# Weather Insights 🌤️ 🌦️

A simple CLI tool that fetches weather forecasts using the [Open-Meteo API](https://open-meteo.com/). It supports geocoding (city + country → coordinates), JSON/CSV export, basic temperature statistics, and short natural-language weather reports generated with OpenAI.



## Features

 - **Geocoding**: Convert city + country into latitude/longitude automatically  
 - **Data export**: Save forecasts as JSON, CSV, or both  
 - **Statistics**: Minimum, maximum, and average temperature  
 - **LLM weather reports**: Automatically generate a short summary with OpenAI  



## Installation

 # Clone the repository:
   git clone https://github.com/GeorgeMrls/AI_Integrator_Portfolio.git
   cd AI_Integrator_Portfolio/weather_insights

 # Create and activate a virtual environment:
  python3.12 -m venv venv312
  source venv312/bin/activate

 # Install dependencies:
  pip install -r src/requirements.txt

 # Set your OpenAI API key (only required for LLM reports):
  export OPENAI_API_KEY="your_api_key_here"



## Usage

  # Basic example
  python src/meteo_fetch.py --city Athens --country GR --format both

  # Limit forecast hours
  python src/meteo_fetch.py --city Thessaloniki --country GR --hours 12 --format json

  # Generate an LLM report
  python src/meteo_fetch.py --city Athens --country GR --report llm --format both



## Arguments
	•	--city (required) → City name (e.g., Athens)
	•	--country (required) → ISO-2 country code (e.g., GR, US)
	•	--hours → Limit forecast to N hours (optional ready for action in the code)
	•	--format → json, csv, both
	•	--report → txt, md, llm
	•	--model → OpenAI model (default: gpt-4.1-mini)
	•	--verbose → Enable detailed logs


## Example output files

  	•	athens_weather.json
	•	athens_weather.csv
	•	athens_weather.md (LLM report)


## Requirements
	•	Python 3.12
	•	Dependencies: requests, openai, pydantic

