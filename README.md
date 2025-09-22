

# Weather Insights 🌦️

A small CLI tool that fetches weather data from [Open-Meteo](https://open-meteo.com/) and can export it to **JSON/CSV** or even create a short **AI-generated weather report** with OpenAI.

---

## What it does
- Look up a **city + country** → get forecast automatically  
- Save results as **JSON**, **CSV**, or **both**  
- Show simple stats (min / max / average temperature)  
- Optionally: let an **LLM** write a short summary  

---

## How to run
 Create a virtual environment & install requirements:
   
   python3.12 -m venv venv312
   source venv312/bin/activate
   pip install -r src/requirements.txt

   Set your OpenAi key to reports:
   export OPENAI_API_KEY="your_api_key_here"

   Run
   python src/meteo_fetch.py --city Athens --country GR --format both --report llm

Example output
	•	athens_weather.json
	•	athens_weather.csv
	•	athens_weather.md (AI summary)
