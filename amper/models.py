from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50)
    consumption = models.PositiveIntegerField()


class NasaReport(models.Model):
    date = models.DateField()


class Report(models.Model):
    item = models.ForeignKey("Item")
    start_time = models.TimeField()
    duration = models.PositiveIntegerField(help_text="in minutes")
    consumption = models.PositiveIntegerField(blank=True, null=True)


class CapacityHour(models.Model):
    hour = models.TimeField()
    capacity = models.PositiveIntegerField()


class Day(models.Model):
    date = models.DateField(unique=True)
    reports = models.ManyToManyField("Report")
    capacity_hours = models.ManyToManyField("CapacityHour")
