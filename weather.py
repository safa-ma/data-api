
import sys
import urllib.parse
import requests

BASE_URI = "https://weather.lewagon.com"


def search_city(query):
    '''
    Look for a given city. If multiple options are returned, have the user choose between them.
    Return one city (or None)
    '''
    try:
        url = f"{BASE_URI}/geo/1.0/direct?q={query}&limit=5"
        response = requests.get(url, timeout=10).json()
        if not response:
            print(f"Error: City '{query}' not found.")
            return None
        if len(response) > 1:
            print("Multiple matches found, which city did you mean?")
            for i, city in enumerate(response, 1):
                country = city.get('country', 'N/A')
                print(f"{i}. {city['name']}, {country}")

            try:
                choice = int(input("> "))
                if 1 <= choice <= len(response):
                    return response[choice - 1]
                print("Invalid choice. Using first city.")
                return response[0]
            except ValueError:
                print("Invalid input. Using first city.")
                return response[0]
        return response[0]

    except requests.exceptions.RequestException as e:
        print(f"Error searching for city: {e}")
        return None

def weather_forecast(lat, lon):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''
    try:
        url = f"{BASE_URI}/data/2.5/forecast?lat={lat}&lon={lon}"
        response = requests.get(url, timeout=10).json()
        daily_forecasts = []
        seen_dates = set()

        for forecast in response['list']:
            date = forecast['dt_txt'].split()[0]
            if "12:00:00" in forecast['dt_txt'] and date not in seen_dates:
                daily_forecasts.append(forecast)
                seen_dates.add(date)
                if len(daily_forecasts) == 5:
                    break
        return daily_forecasts
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather forecast: {e}")
        return []

def main():
    '''Ask user for a city and display weather forecast'''
    query = input("City?\n> ")
    city = search_city(query)
    query = input("City?\n> ").strip()

    if not query:
        return

    city = search_city(query)
    if not city:
        return

    forecasts = weather_forecast(city['lat'], city['lon'])
    if not forecasts:
        print("No weather forecast available.")
        return

    print(f"\nHere's the weather in {city['name']}:")
    for forecast in forecasts:
        date = forecast['dt_txt'].split()[0]
        weather = forecast['weather'][0]['description']
        temp = int(round(forecast['main']['temp_max']))
        print(f"{date}: {weather} ({temp}°C)")

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
