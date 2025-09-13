# AI Integrator Portfolio
# PDF Insights – AI Integrator Portfolio

A simple Python tool that fetches Athens weather data from the Open-Meteo API and saves it as JSON.  
This project demonstrates API integration, project structuring, and version control with Git.

---

## Features
- Fetch weather data via Open-Meteo API  
- Save output to `src/data/athens_weather.json`  
- Clear folder structure for learning and extension  

---

## Project Structure
pdf_insights/
├── Postman/               # Postman collections
├── src/
│   ├── meteo_fetch.py     # Main script
│   └── data/              # JSON output
├── requirements.txt       # Python dependencies
└── README.md

---

## Quick Start
```bash
# Clone the repo
git clone https://github.com/GeorgeMrls/AI_Integrator_Portfolio.git

# Navigate to project
cd AI_Integrator_Portfolio/pdf_insights

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run script
python src/meteo_fetch.py

# The script generates
src/data/athens_weather.json
'''