from __future__ import unicode_literals

from django.utils import timezone
from rest_framework import serializers
from rest_framework.decorators import detail_route, list_route

from amper import utils
from amper.models import Item, Report, CapacityHour, Day, UserConfig, RealTimeData
from amper.utils import time_round


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
    date = serializers.DateTimeField(required=False)
    reports = ReportSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        report_data = self.context["request"].data.get("report")
        item_data = report_data["item"]

        report_data["item"] = Item.objects.get(pk=int(item_data.get("id")))

        report = Report.objects.create(**report_data)

        instance.reports.add(report)
        return instance

    class Meta:
        model = Day
        fields = ("id", "reports", "capacity", "date")


class RealTimeDataSerializer(utils.RelationModelSerializer):

    class Meta:
        model = RealTimeData
        fields = ("id", "consumption", "produced")


class UserConfigSerializer(serializers.ModelSerializer):
    azimut = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    solar_panel_angle = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    reflectance_angle = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)

    def create(self, validated_data):
        config = UserConfig.objects.all()
        if config.exists():
            config.update(**validated_data)
            return config.first()
        else:
            return super(UserConfigSerializer, self).create(validated_data=validated_data)

    class Meta:
        model = UserConfig
        fields = ("latitude", "azimut", "solar_panel_angle", "reflectance_angle", "square_meters")
