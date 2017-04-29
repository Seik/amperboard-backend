from __future__ import unicode_literals

from rest_framework import serializers

from amper import utils
from amper.models import Item, Report, CapacityHour, Day


class ItemSerializer(utils.RelationModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "consumption")


class ReportSerializer(utils.RelationModelSerializer):
    item = ItemSerializer(is_relation=True)

    def create(self, validated_data):
        return super(ReportSerializer, self).create(validated_data=validated_data)

    class Meta:
        model = Report
        fields = ("id", "item", "start_time", "duration", "consumption")


class CapacityHourSerializer(utils.RelationModelSerializer):
    class Meta:
        model = CapacityHour
        fields = ("id", "hour", "capacity")


class DaySerializer(utils.RelationModelSerializer):
    class Meta:
        model = Day
        fields = ("id", "reports", "capacity_hours")
