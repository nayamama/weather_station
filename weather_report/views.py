from django.shortcuts import render
import pytz
from django.http import Http404

from .weather import get_current_city_weather_data, get_five_days_forecast

tz_china = pytz.timezone('Asia/Shanghai')
tz_east = pytz.timezone('America/Toronto')
tz_west = pytz.timezone('America/Los_Angeles')


def index(request):
    harbin_report = get_current_city_weather_data('harbin')
    montreal_report = get_current_city_weather_data('montreal')
    sandiego_report = get_current_city_weather_data('San Diego')
    return render(request,
                  'weather_report/index.html',
                  {'harbin_report': harbin_report,
                   'montreal_report': montreal_report,
                   'sandiego_report': sandiego_report})


def detail(request, city=None):
    report = dict()
    if request.method == 'POST':
        city = request.POST['city']
        report = get_five_days_forecast(city)
        if report['cod'] == 404:
            raise Http404()
        else:
            city = city.title()
    return render(request, 'weather_report/detail.html', {'report': report, 'city': city})
