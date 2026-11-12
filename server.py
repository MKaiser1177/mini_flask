from flask import Flask, render_template, request
from weather import get_current_weather

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/weather")
def weather():
    city = request.args.get("city", "").strip()

    if not city:
        city = "Mumbai"

    weather_data = get_current_weather(city)
    cod = weather_data.get("cod") if isinstance(weather_data, dict) else None

    if isinstance(cod, str):
        try:
            cod = int(cod)
        except ValueError:
            cod = None

    if not weather_data or cod != 200:
        return render_template("city-not-found.html")

    weather_info = weather_data.get("weather", [{}])[0]
    main_info = weather_data.get("main", {})

    return render_template(
        "weather.html",
        title=weather_data.get("name", city),
        status=weather_info.get("description", "Clear").capitalize(),
        temp=f"{main_info.get('temp', 0):.1f}",
        feels_like=f"{main_info.get('feels_like', 0):.1f}",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)