from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from amper.models import Item, Report, CapacityHour, Day
from amper.resources import ItemResource


@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):
    resource_class = ItemResource


admin.site.register(Report, admin.ModelAdmin)
admin.site.register(CapacityHour, admin.ModelAdmin)
admin.site.register(Day, admin.ModelAdmin)
