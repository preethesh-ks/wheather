import json
import socket
import requests
from flask import Flask, render_template, redirect

app = Flask(__name__)
apiKey = "dd4b4c90728f44888fa161932230104"


def getCondition(conditionText):
    conditionText = conditionText.lower()
    if "rain with thunder" in conditionText or "thundery" in conditionText:
        return "⛈️"
    elif "rain" in conditionText or "drizzle" in conditionText:
        return "🌧️"
    elif "sun" in conditionText or "sunny" in conditionText or "clear" in conditionText:
        return "☀️"
    elif (
        "cloud" in conditionText
        or "cloudy" in conditionText
        or "overcast" in conditionText
    ):
        return "☁️"
    elif (
        "snow" in conditionText
        or "snowy" in conditionText
        or "sleet" in conditionText
        or "blizzard" in conditionText
    ):
        return "🌨️"
    elif "fog" in conditionText or "foggy" in conditionText or "mist" in conditionText:
        return "🌫️"
    elif "pellets" in conditionText:
        return "❄️"
    else:
        return conditionText


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/weather/<location>")
def weather(location):
    api = requests.get(
        f"http://api.weatherapi.com/v1/forecast.json?key={apiKey}&q={location}&days=8&aqi=no&alerts=no"
    )
    if api.status_code == 400:
        return redirect("/")
    data = json.loads(api.text)
    current = data["current"]
    location = data["location"]
    day1 = data["forecast"]["forecastday"][1]
    day2 = data["forecast"]["forecastday"][2]
    day3 = data["forecast"]["forecastday"][3]
    day4 = data["forecast"]["forecastday"][4]
    day5 = data["forecast"]["forecastday"][5]
    day6 = data["forecast"]["forecastday"][6]
    day7 = data["forecast"]["forecastday"][7]
    return render_template(
        "weather.html",
        currentTemp=current["temp_c"],
        locationName=location["name"],
        localTime=location["localtime"].split(" ")[1],
        locationRegion=location["region"],
        locationCountry=location["country"],
        currentCondition=getCondition(current["condition"]["text"]),
        data=[
            [
                getCondition(day1["day"]["condition"]["text"]),
                day1["day"]["avgtemp_c"],
                day1["day"]["maxtemp_c"],
                day1["day"]["mintemp_c"],
                day1["date"].replace("-", "/")[5:],
            ],
            [
                getCondition(day2["day"]["condition"]["text"]),
                day2["day"]["avgtemp_c"],
                day2["day"]["maxtemp_c"],
                day2["day"]["mintemp_c"],
                day2["date"].replace("-", "/")[5:],
            ],
            [
                getCondition(day3["day"]["condition"]["text"]),
                day3["day"]["avgtemp_c"],
                day3["day"]["maxtemp_c"],
                day3["day"]["mintemp_c"],
                day3["date"].replace("-", "/")[5:],
            ],
            [
                getCondition(day4["day"]["condition"]["text"]),
                day4["day"]["avgtemp_c"],
                day4["day"]["maxtemp_c"],
                day4["day"]["mintemp_c"],
                day4["date"].replace("-", "/")[5:],
            ],
            [
                getCondition(day5["day"]["condition"]["text"]),
                day5["day"]["avgtemp_c"],
                day5["day"]["maxtemp_c"],
                day5["day"]["mintemp_c"],
                day5["date"].replace("-", "/")[5:],
            ],
            [
                getCondition(day6["day"]["condition"]["text"]),
                day6["day"]["avgtemp_c"],
                day6["day"]["maxtemp_c"],
                day6["day"]["mintemp_c"],
                day6["date"].replace("-", "/")[5:],
            ],
            [
                getCondition(day7["day"]["condition"]["text"]),
                day7["day"]["avgtemp_c"],
                day7["day"]["maxtemp_c"],
                day7["day"]["mintemp_c"],
                day7["date"].replace("-", "/")[5:],
            ],
        ],
    )


@app.errorhandler(404)
def pageNotFound(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(
        debug=True,
        host=socket.gethostbyname(socket.gethostname()),
    )
