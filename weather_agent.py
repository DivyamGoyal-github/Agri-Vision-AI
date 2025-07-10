#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests

# --- API KEYS ---
OPENWEATHER_API_KEY = "ece1b5b548bb8a9ac6eaae428205ec46"
WEATHERBIT_API_KEY = "01b3dd6d1aba488e8cccfb2148414d69"
TOMORROW_API_KEY = "uyGFzqaXSuQ7abQpG1d8ASPzsREIgoQ8"

# --- FETCH FUNCTIONS ---
def fetch_openweather(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].capitalize()
        }
    except Exception as e:
        return {"error": f"OpenWeatherMap error: {str(e)}"}

def fetch_weatherbit(lat, lon):
    try:
        url = f"https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&key={WEATHERBIT_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()["data"][0]
        return {
            "temperature": data["temp"],
            "humidity": data["rh"],
            "solar_rad": data.get("solar_rad", "N/A"),
            "soil_temp": data.get("soil_temp", "N/A"),
            "description": data["weather"]["description"]
        }
    except Exception as e:
        return {"error": f"Weatherbit error: {str(e)}"}

def fetch_tomorrow_io(lat, lon):
    try:
        url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={TOMORROW_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get("data", {}).get("values", {})
        return {
            "temperature": data.get("temperature", "N/A"),
            "humidity": data.get("humidity", "N/A"),
            "rain_probability": data.get("precipitationProbability", "N/A"),
            "soil_moisture": data.get("soilMoistureVolumetric0To10cm", "N/A"),
            "evapotranspiration": data.get("evapotranspiration", "N/A")
        }
    except Exception as e:
        return {"error": f"Tomorrow.io error: {str(e)}"}

# --- MAIN FUNCTION (Agent-friendly) ---
def get_weather_info(lat, lon) -> str:
    openweather = fetch_openweather(lat, lon)
    weatherbit = fetch_weatherbit(lat, lon)
    tomorrow = fetch_tomorrow_io(lat, lon)

    report = f"\n🌾 Combined Weather Insights for Location ({lat}, {lon}):\n"

    if "error" not in openweather:
        report += f"""
🧩 OpenWeatherMap:
- Temp: {openweather['temperature']}°C
- Humidity: {openweather['humidity']}%
- Description: {openweather['description']}"""

    if "error" not in weatherbit:
        report += f"""
🌤️ Weatherbit:
- Temp: {weatherbit['temperature']}°C
- Humidity: {weatherbit['humidity']}%
- Solar Radiation: {weatherbit['solar_rad']} W/m²
- Soil Temp: {weatherbit['soil_temp']}°C
- Description: {weatherbit['description']}"""

    if "error" not in tomorrow:
        report += f"""
🛰️ Tomorrow.io:
- Temp: {tomorrow['temperature']}°C
- Humidity: {tomorrow['humidity']}%
- Rain Probability: {tomorrow['rain_probability']}%
- Soil Moisture: {tomorrow['soil_moisture']} m³/m³
- Evapotranspiration: {tomorrow['evapotranspiration']} mm/day"""

    # Add any API errors
    for api_response in [openweather, weatherbit, tomorrow]:
        if "error" in api_response:
            report += f"\n\n⚠️ {api_response['error']}"

    return report


# In[ ]:





# In[ ]:




