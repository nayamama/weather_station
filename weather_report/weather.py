from requests import request
from datetime import datetime
import pytz
import environ

env = environ.Env()
environ.Env.read_env(env_file='../weather_center/.env')

API_KEY = env('WEATHER_API_KEY')

# create the time zones
tz_china = pytz.timezone('Asia/Shanghai')
tz_east = pytz.timezone('America/Toronto')
tz_west = pytz.timezone('America/Los_Angeles')


def get_current_city_weather_data(city, tz):
    result = dict()
    query_str = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(city, API_KEY)
    response = request('GET', query_str)
    data = response.json()
    result['weather'] = data['weather'][0]['description']
    result['temp'] = data['main']['temp']
    result['feels_like'] = data['main']['feels_like']
    result['wind'] = '{} KM/H'.format(round(data['wind']['speed'] * 3.6, 2))
    sunrise = datetime.fromtimestamp(data['sys']['sunrise'])
    sunset = datetime.fromtimestamp(data['sys']['sunset'])
    result['sun_rise_local'] = sunrise.astimezone(tz).strftime('%H: %M')
    result['sun_set_local'] = sunset.astimezone(tz).strftime('%H: %M')

    return result
