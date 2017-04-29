from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.response import Response

from amper.models import Item, Report
from amper.serializers import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class PastDayViewSet(viewsets.ViewSet):
    def list(self, request):
        date = request.query_params.get("date")
        return Response(status=200)
