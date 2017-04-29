from __future__ import unicode_literals

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from amper.viewsets import ItemViewSet

router = DefaultRouter()

router.register(r'items', ItemViewSet, 'items')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
