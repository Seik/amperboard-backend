from __future__ import unicode_literals

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from amper.models import Item, Report, CapacityHour, Day, UserConfig, RealTimeData
from amper.resources import ItemResource


@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):
    resource_class = ItemResource


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    filter_horizontal = ("reports",)


admin.site.register(Report, admin.ModelAdmin)
admin.site.register(CapacityHour, admin.ModelAdmin)
admin.site.register(UserConfig, admin.ModelAdmin)
admin.site.register(RealTimeData, admin.ModelAdmin)
