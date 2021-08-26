from django.shortcuts import render
from django.http import Http404
from django.conf import settings

from .weather import get_current_city_weather_data, get_five_days_forecast
from .forms import AdvancedSearchForm
from .google_api import GoogleMapsClient


def index(request):
    data = {}
    for city in ['harbin', 'montreal', 'san diego']:
        query_str = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(city,
                                                                                                       settings.WEATHER_API_KEY)
        data[city.split()[0] + '_report'] = get_current_city_weather_data(query_str)
    return render(request,
                  'weather_report/index.html',
                  {'data': data})


def detail(request):
    if request.method == "POST":
        location = None
        city = request.POST['city']
        if request.POST['country']:
            country_code = request.POST['country']
            location = ','.join([city, country_code])
        else:
            location = city
        client = GoogleMapsClient(api_key=settings.GOOGLE_API_KEY, address_or_zip=location)

        # construct two query strings for weather API
        current_query_str = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}'.format(
            client.lat, client.lng, settings.WEATHER_API_KEY)
        trend_query_str = 'http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units=metric&appid={}'.format(
            client.lat, client.lng, settings.WEATHER_API_KEY)

        # construct query string for embed Google Map
        embed_map_query_str = "https://www.google.com/maps/embed/v1/place?key={}&q={}".format(settings.GOOGLE_API_KEY,
                                                                                              location)

        # retrieve single point report and trend chart
        current_report = get_current_city_weather_data(current_query_str)
        trend_report = get_five_days_forecast(trend_query_str)
        if current_report['cod'] == 404:
            raise Http404()

        restaurants = client.get_top_5_places()

        city = city.title()

        return render(request, 'weather_report/detail.html',
                      {'current_report': current_report, 'trend_report': trend_report, 'city': city,
                       'embed_map_query_str': embed_map_query_str, 'restaurants': restaurants})
    else:
        form = AdvancedSearchForm()
    return render(request, 'weather_report/advanced_search_modal.html', {'form': form})
