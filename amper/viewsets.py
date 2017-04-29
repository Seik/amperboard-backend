from __future__ import unicode_literals

from datetime import datetime, timedelta

from rest_framework import viewsets
from rest_framework.response import Response

from amper.models import Item, Report
from amper.serializers import ItemSerializer, ReportSerializer


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class PastDayViewSet(viewsets.ViewSet):
    def list(self, request):
        reports = Report.objects.filter(start_time__gte=datetime.now() - timedelta(1))

        json_response = []

        for report in reports:
            json_response.append({
                "id": report.pk,
                "item": report.item.name,
                "consumption": report.item.consumption,
                "time": report.start_time.time()
            })

        return Response(json_response)
