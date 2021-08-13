from django.shortcuts import render
import pytz

from .weather import get_current_city_weather_data

tz_china = pytz.timezone('Asia/Shanghai')
tz_east = pytz.timezone('America/Toronto')
tz_west = pytz.timezone('America/Los_Angeles')


def index(request):
    if request.method == 'POST':
        city = request.POST['city']
    else:
        harbin_report = get_current_city_weather_data('harbin', tz_china)
        montreal_report = get_current_city_weather_data('montreal', tz_east)
        sandiego_report = get_current_city_weather_data('San Diego', tz_west)
        return render(request,
                      'weather_report/index.html',
                      {'harbin_report': harbin_report,
                       'montreal_report': montreal_report,
                       'sandiego_report': sandiego_report})
