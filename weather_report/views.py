from django.shortcuts import render


def index(request):
    return render(request, 'weather_report/index.html')
