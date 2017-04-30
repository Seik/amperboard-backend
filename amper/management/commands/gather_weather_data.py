from __future__ import unicode_literals

import datetime
from os import environ

import requests
from django.core.management.base import BaseCommand

from amper.models import WeatherData


class Command(BaseCommand):
    def handle(self, *args, **options):
        api_key = environ.get("OWM_API_KEY")

        url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=Valencia,46018&cnt=16&units=metric&APPID=" + api_key

        r = requests.get(url)

        city = r.json()["city"]["name"]

        for obj in r.json()["list"]:
            weather = WeatherData.objects.create(city=city,
                                                 date=datetime.datetime.fromtimestamp(obj["dt"]),
                                                 temp_max=obj["temp"]["max"],
                                                 temp_min=obj["temp"]["min"],
                                                 pressure=obj["pressure"],
                                                 humidity=obj["humidity"],
                                                 wind_speed=obj["speed"]
                                                 )
