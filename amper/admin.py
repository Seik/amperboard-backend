from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from amper.models import Item, Report, CapacityHour, Day, UserConfig
from amper.resources import ItemResource


@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):
    resource_class = ItemResource


@admin.register(UserConfig)
class UserConfigAdmin(admin.ModelAdmin):
    pass


admin.site.register(Report, admin.ModelAdmin)
admin.site.register(CapacityHour, admin.ModelAdmin)
admin.site.register(Day, admin.ModelAdmin)
