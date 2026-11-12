import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()


def get_current_weather(city="Mumbai"):
    api_key = os.getenv("API_KEY")
    if not api_key:
        return {"cod": 401, "message": "API key is missing"}

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": api_key, "units": "metric"},
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException:
        return {"cod": 500, "message": "Unable to fetch weather data"}

    try:
        weather_data = response.json()
    except ValueError:
        return {"cod": 500, "message": "Invalid weather API response"}

    return weather_data


if __name__ == "__main__":
    weather_data = get_current_weather()
    pprint(weather_data)

