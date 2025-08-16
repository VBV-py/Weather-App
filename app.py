from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

app = Flask(__name__)

BASE_URL = "http://api.weatherapi.com/v1/forecast.json"

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    forecast_days = None

    if request.method == "POST":
        city = request.form.get("city")
        forecast_choice = request.form.get("forecast_days")  

        days = int(forecast_choice) if forecast_choice else 1

        if city:
            params = {
                "key": API_KEY,
                "q": city,
                "days": days,
                "aqi": "no",
                "alerts": "no"
            }
            response = requests.get(BASE_URL, params=params)

            if response.status_code == 200:
                data = response.json()

                # Current Weather
                weather = {
                    "city": data["location"]["name"],
                    "country": data["location"]["country"],
                    "last_updated": data["current"]["last_updated"],
                    "temperature": data["current"]["temp_c"],
                    "condition": data["current"]["condition"]["text"],
                    "icon": data["current"]["condition"]["icon"],
                    "feelslike": data["current"]["feelslike_c"],
                    "humidity": data["current"]["humidity"],
                    "wind_kph": data["current"]["wind_kph"],
                    "uv": data["current"]["uv"]
                }

                if days >= 1:
                    forecast_days = []
                    for day in data["forecast"]["forecastday"]:
                        day_data = {
                            "date": day["date"],
                            "day_name": datetime.strptime(day["date"], "%Y-%m-%d").strftime("%A"),
                            "maxtemp_c": day["day"]["maxtemp_c"],
                            "mintemp_c": day["day"]["mintemp_c"],
                            "avgtemp_c": day["day"]["avgtemp_c"],
                            "condition": day["day"]["condition"]["text"],
                            "icon": day["day"]["condition"]["icon"],
                            "uv": day["day"]["uv"]
                        }

                        
                        hours = []
                        for h in day["hour"]:
                            hour_data = {
                                "time": h["time"],
                                "temp_c": h["temp_c"],
                                "condition": h["condition"]["text"],
                                "icon": h["condition"]["icon"]
                            }
                            hours.append(hour_data)

                        day_data["hours"] = hours
                        forecast_days.append(day_data)

            else:
                weather = {"error": "City not found!"}

    return render_template("index.html", weather=weather, forecast_days=forecast_days)

if __name__ == "__main__":
    app.run(debug=True)
