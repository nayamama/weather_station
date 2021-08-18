from requests import request
from datetime import datetime
import matplotlib.pyplot as plt
import pytz
import environ
from io import BytesIO
import base64

env = environ.Env()
environ.Env.read_env(env_file='../weather_center/.env')

API_KEY = env('WEATHER_API_KEY')

# create the time zones
tz_china = pytz.timezone('Asia/Shanghai')
tz_east = pytz.timezone('America/Toronto')
tz_west = pytz.timezone('America/Los_Angeles')


def get_current_city_weather_data(city):
    result = dict()
    query_str = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(city, API_KEY)
    response = request('GET', query_str)
    data = response.json()

    if data['cod'] == '404':
        result['cod'] = 404
    else:
        result['weather'] = data['weather'][0]['description']
        result['temp'] = data['main']['temp']
        result['feels_like'] = data['main']['feels_like']
        result['wind'] = '{} KM/H'.format(round(data['wind']['speed'] * 3.6, 2))
        result['sun_rise_local'] = datetime.fromtimestamp(data['sys']['sunrise'] + data['timezone']).strftime(
            '%H: %M')
        result['sun_set_local'] = datetime.fromtimestamp(data['sys']['sunset'] + data['timezone']).strftime(
            '%H: %M')
        # get current time from UTC timestamp and time zone offset
        utc = datetime.utcnow().timestamp()
        time_str = datetime.fromtimestamp(utc + data['timezone']).strftime("%A, %B %d, %H: %M")
        result['local_time'] = time_str
        result['country'] = data['sys']['country']

    return result


def get_five_days_forecast(city):
    result = get_current_city_weather_data(city)
    if result['cod'] != 404:
        query_str = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid={}'.format(city, API_KEY)
        response = request('GET', query_str)
        data = response.json()

        temp = []
        feels = []
        weather = []
        date = []

        for ind, elem in enumerate(data['list']):
            if ind % 4 == 0:
                temp.append(elem['main']['temp'])
                feels.append(elem['main']['feels_like'])
                weather.append(elem['weather'][0]['description'])
                date.append(elem['dt_txt'][5:16])

        fig = plt.figure(figsize=(15, 8))
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twiny()

        tickers = [i for i in range(len(date))]

        ax1.plot(date, temp, marker="o", label="Actual temp")
        ax1.plot(date, feels, marker='o', label="Feels like")
        ax1.legend(loc='upper left', prop={'size': 15})
        ax1.set_xticklabels(date, rotation=90)
        # ax1.set_ylim((10, 35))

        ax2.set_xlim(ax1.get_xlim())
        ax2.set_xticks(tickers)
        ax2.set_xticklabels([l + "\n" * (i % 2) for i, l in enumerate(weather)])

        ax1.set_title("Every 12-Hours Forecast for 5 Days", fontsize=30, pad=20)
        plt.grid()
        plt.tight_layout()

        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)

        img = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(img)
        graphic = graphic.decode('utf-8')

        result['chart'] = graphic

    return result
