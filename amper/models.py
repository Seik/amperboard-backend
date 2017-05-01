from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Item(models.Model):
    name = models.CharField(max_length=50)
    consumption = models.PositiveIntegerField()

    def __str__(self):
        return "{} - {}".format(self.name, self.consumption)


@python_2_unicode_compatible
class Report(models.Model):
    item = models.ForeignKey("Item")
    start_time = models.DateTimeField()
    duration = models.PositiveIntegerField(help_text="in minutes")
    consumption = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.item, self.consumption)


@python_2_unicode_compatible
class CapacityHour(models.Model):
    hour = models.DateTimeField(unique=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return "{} - {}".format(self.hour, self.capacity)


@python_2_unicode_compatible
class Day(models.Model):
    date = models.DateField(unique=True)
    reports = models.ManyToManyField("Report", blank=True)
    capacity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.date)


@python_2_unicode_compatible
class RealTimeData(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True, unique=True)
    consumption = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    produced = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return "{} {} {}".format(self.date, self.consumption, self.produced)


@python_2_unicode_compatible
class WeatherData(models.Model):
    date = models.DateTimeField(unique=True)
    city = models.CharField(max_length=50)
    temp_max = models.DecimalField(max_digits=5, decimal_places=2)
    temp_min = models.DecimalField(max_digits=5, decimal_places=2)
    pressure = models.DecimalField(max_digits=6, decimal_places=2)
    wind_speed = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return "{} {} {} {} {} {} {}".format(self.date, self.city, self.temp_max, self.temp_min, self.pressure,
                                             self.humidity, self.wind_speed)


class UserConfig(models.Model):
    latitude = models.IntegerField()
    azimut = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    solar_panel_angle = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    reflectance_angle = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    square_meters = models.DecimalField(max_digits=20, decimal_places=2)
