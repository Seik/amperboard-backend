from __future__ import unicode_literals

from amper import utils
from amper.models import Item, Report, CapacityHour, Day


class ItemSerializer(utils.RelationModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "consumption")


class ReportSerializer(utils.RelationModelSerializer):
    item = ItemSerializer(is_relation=True)

    class Meta:
        model = Report
        fields = ("id", "item", "start_time", "duration", "consumption", "completed")


class CapacityHourSerializer(utils.RelationModelSerializer):
    class Meta:
        model = CapacityHour
        fields = ("id", "hour", "capacity")


class DaySerializer(utils.RelationModelSerializer):
    class Meta:
        model = Day
        fields = ("id", "reports", "capacity_hours")
