from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Item(models.Model):
    name = models.CharField(max_length=50)
    consumption = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Report(models.Model):
    item = models.ForeignKey("Item")
    start_time = models.TimeField()
    duration = models.PositiveIntegerField(help_text="in minutes")
    consumption = models.PositiveIntegerField(blank=True, null=True)
    completed = models.BooleanField(default=False)


class CapacityHour(models.Model):
    hour = models.TimeField()
    capacity = models.PositiveIntegerField()


class Day(models.Model):
    date = models.DateField(unique=True)
    reports = models.ManyToManyField("Report")
    capacity_hours = models.ManyToManyField("CapacityHour")
