from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50)
    consumption = models.PositiveIntegerField()


