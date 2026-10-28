
import requests

def get_weather(city):
    try:
        # Find the city coordinates
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_response = requests.get(
            geo_url,
            params={"name": city, "count": 1},
            timeout=10
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            print("City not found. Please enter a valid city.")
            return

        location = geo_data["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]

        # Get current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_response = requests.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,"
                           "apparent_temperature,is_day,precipitation,"
                           "weather_code,wind_speed_10m"
            },
            timeout=10
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current"]

        print("\n--- Weather Report ---")
        print("City:", city_name)
        print("Temperature:", current["temperature_2m"], "°C")
        print("Feels Like:", current["apparent_temperature"], "°C")
        print("Humidity:", current["relative_humidity_2m"], "%")
        print("Wind Speed:", current["wind_speed_10m"], "km/h")
        print("Precipitation:", current["precipitation"], "mm")

    except requests.exceptions.Timeout:
        print("Request timed out. Please try again.")

    except requests.exceptions.RequestException:
        print("Unable to connect to the weather service.")

    except (KeyError, IndexError, ValueError):
        print("Unable to process weather data.")


city = input("Enter city name: ").strip()

if city:
    get_weather(city)
else:
    print("City name cannot be empty.")
