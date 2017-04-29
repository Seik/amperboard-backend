from __future__ import unicode_literals

from rest_framework import viewsets

from amper.models import Item
from amper.serializers import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
