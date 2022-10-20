from flask import current_app
import requests
from pprint import pprint


def get_weather_by_city(city_name):
    url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'
    params = {
        'key': current_app.config['WEATHER_APY_KEY'],
        'q': city_name,
        'format': 'json',
        'num_of_days': 1,
        'lang': 'en'
    }
    try:
        result = requests.get(url, params=params)
        result.raise_for_status()
        weather = result.json()
    except (requests.RequestException, ValueError):
        return False
    if 'data' in weather:
        if 'current_condition' in weather['data']:
            try:
                return weather['data']['current_condition'][0]
            except (IndexError, TypeError):
                return False
    return False


if __name__ == '__main__':
    pprint(get_weather_by_city('China,Beijing'))
else:
    'imported'

