from __future__ import unicode_literals

import time
from datetime import timedelta

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from amper.models import Item, Report, UserConfig, Day, CapacityHour, RealTimeData
from amper.serializers import ItemSerializer, ReportSerializer, UserConfigSerializer, DaySerializer, \
    CapacityHourSerializer, RealTimeDataSerializer


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    @list_route()
    def on_items(self, request):
        real_time_data = RealTimeData.objects.order_by("-pk")[0]

        items = []
        if 5 < real_time_data.consumption < 14:
            items = Item.objects.filter(pk=8)
        elif 14 < real_time_data.consumption < 25:
            items = Item.objects.filter(pk=5)
        elif real_time_data.consumption > 25:
            items = Item.objects.filter(pk__in=[5, 8])

        json_data = []

        for item in items:
            json_data.append({
                "id": item.pk,
                "name": item.name,
                "consumption": real_time_data.consumption
            })

        return Response(json_data)


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    @list_route()
    def past_day(self, request):
        reports = self.queryset.filter(start_time__gte=timezone.now() - timedelta(1))

        json_response = []

        for report in reports:
            json_response.append({
                "id": report.pk,
                "item": ItemSerializer(report.item).data,
                "consumption": report.consumption,
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
        queryset = self.queryset.filter(hour__gte=timezone.now() - timedelta(1)) & self.queryset.filter(
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


class RealTimeDataViewSet(viewsets.ModelViewSet):
    serializer_class = RealTimeDataSerializer
    queryset = RealTimeData.objects.all()

    @list_route()
    def recent(self, request):
        recent_data = RealTimeData.objects.all().order_by("date").first()

        serializer_data = RealTimeDataSerializer(recent_data)
        return Response(serializer_data.data)

    @list_route()
    def post_from_arduino(self, request):
        consumption = request.query_params.get("consumption")
        produced = request.query_params.get("produced")

        '''
        data = RealTimeData.objects.all().first()

        if data is not None:
            data.consumption = consumption
            data.produced = produced
            data.date = timezone.now()

            data.save()

            return Response(status=201)
        '''

        RealTimeData.objects.create(consumption=consumption, produced=produced)
        return Response(status=201)


class UserConfigViewSet(viewsets.ModelViewSet):
    serializer_class = UserConfigSerializer
    queryset = UserConfig.objects.all()
