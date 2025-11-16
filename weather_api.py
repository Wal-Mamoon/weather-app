import os
import requests
from datetime import datetime

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"


def get_weather(city):
    if not API_KEY:
        return {"error": "API key is not configured"}

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}

    if "list" not in weather_data or not weather_data["list"]:
        return {"error": "City not found or API issue"}

    # Process the 3-hour data to get a 5-day summary
    daily_forecasts = {}
    for forecast_item in weather_data.get("list", []):
        day_date = forecast_item["dt_txt"].split(" ")[0]
        if day_date not in daily_forecasts:
            daily_forecasts[day_date] = {
                "day": datetime.fromisoformat(day_date).strftime('%A'),
                "temps": [],
                "rain_chances": [],
                "weathers": {}
            }
        daily_forecasts[day_date]["temps"].append(
            forecast_item["main"]["temp"])
        daily_forecasts[day_date]["rain_chances"].append(
            forecast_item.get("pop", 0))
        weather_desc = forecast_item["weather"][0]["description"]
        daily_forecasts[day_date]["weathers"][weather_desc] = daily_forecasts[day_date]["weathers"].get(
            weather_desc, 0) + 1

    # Consolidate daily data
    final_forecasts = [{
        "day": data["day"], "temp_max": max(data["temps"]), "temp_min": min(data["temps"]),
        "rain_chance": max(data["rain_chances"]) * 100, "weather": max(data["weathers"], key=data["weathers"].get)
    } for data in daily_forecasts.values()]

    return {
        "city": weather_data["city"]["name"],
        "forecasts": final_forecasts
    }
