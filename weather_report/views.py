from django.shortcuts import render
import pytz
from django.http import Http404
import environ

from .weather import get_current_city_weather_data, get_five_days_forecast
from .forms import AdvancedSearchForm

env = environ.Env()
environ.Env.read_env(env_file='../weather_center/.env')

API_KEY = env('WEATHER_API_KEY')

tz_china = pytz.timezone('Asia/Shanghai')
tz_east = pytz.timezone('America/Toronto')
tz_west = pytz.timezone('America/Los_Angeles')


def index(request):
    data = {}
    for city in ['harbin', 'montreal', 'san diego']:
        query_str = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(city, API_KEY)
        data[city.split()[0] + '_report'] = get_current_city_weather_data(query_str)
    return render(request,
                  'weather_report/index.html',
                  {'data': data})


def detail(request):
    city = None
    if request.method == 'POST':
        city = request.POST['city']
    current_query_str = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(city,
                                                                                                           API_KEY)
    trend_query_str = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid={}'.format(city,
                                                                                                          API_KEY)
    current_report = get_current_city_weather_data(current_query_str)
    trend_report = get_five_days_forecast(trend_query_str)
    if current_report['cod'] == 404:
        raise Http404()

    city = city.title()

    return render(request, 'weather_report/detail.html',
                  {'current_report': current_report, 'trend_report': trend_report, 'city': city})


def advanced_search(request):
    if request.method == "POST":
        country_code = request.POST['country']
        city = request.POST['city']

        query_str = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'.format(45.4947222,
                                                                                                   -73.5654918, API_KEY)
    else:
        form = AdvancedSearchForm()
        return render(request, 'weather_report/advanced_search_modal.html', {'form': form})
