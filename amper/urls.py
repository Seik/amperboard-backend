from __future__ import unicode_literals

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from amper.viewsets import ItemViewSet, RequestViewSet, UserConfigViewSet, DayViewSet

router = DefaultRouter()

router.register(r'items', ItemViewSet, 'items')
router.register(r'reports', RequestViewSet, 'reports')
router.register(r'days', DayViewSet, 'days')
router.register(r'user-config', UserConfigViewSet, 'user-config')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
