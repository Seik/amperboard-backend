from __future__ import unicode_literals

import time
from datetime import timedelta

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from amper.models import Item, Report, UserConfig, Day, CapacityHour
from amper.serializers import ItemSerializer, ReportSerializer, UserConfigSerializer, DaySerializer, \
    CapacityHourSerializer


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    @list_route()
    def past_day(self, request):
        reports = self.queryset.filter(start_time__gte=timezone.now() - timedelta(1))

        json_response = []

        for report in reports:
            json_response.append({
                "id": report.pk,
                "item": report.item.name,
                "consumption": report.item.consumption,
                "time": report.start_time
            })

        return Response(json_response)

    @list_route()
    def pending_tasks(self, request):
        pending_objects = self.queryset.filter(start_time__gte=timezone.now() - timedelta(1))

        json_response = []

        for report in pending_objects:
            now_ts = time.mktime(timezone.now().timetuple())
            task_ts = time.mktime(report.start_time.timetuple()) + (report.duration * 60)
            if task_ts < now_ts:
                json_response.append({
                    "id": report.pk,
                    "item": ItemSerializer(report.item).data,
                    "date": report.start_time
                })

        return Response(json_response)


class CapacityHourViewSet(viewsets.ModelViewSet):
    serializer_class = CapacityHourSerializer
    queryset = CapacityHour.objects.all()

    @list_route()
    def past_day(self, request):
        queryset = self.queryset.filter(hour__gte=timezone.now() - timedelta(hours=24)) | self.queryset.filter(
            hour__lte=timezone.now())
        serializer_data = CapacityHourSerializer(queryset, many=True)
        return Response(serializer_data.data)


class DayViewSet(viewsets.ModelViewSet):
    serializer_class = DaySerializer
    queryset = Day.objects.all()

    @list_route()
    def week(self, request):
        queryset = self.queryset.filter(date__gte=timezone.now() - timedelta(7))
        serializer_data = DaySerializer(queryset, many=True)
        return Response(serializer_data.data)


class UserConfigViewSet(viewsets.ModelViewSet):
    serializer_class = UserConfigSerializer
    queryset = UserConfig.objects.all()
