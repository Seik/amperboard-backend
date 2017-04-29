from django.contrib import admin

from amper.models import Item, Report, CapacityHour, Day

admin.site.register(Item, admin.ModelAdmin)
admin.site.register(Report, admin.ModelAdmin)
admin.site.register(CapacityHour, admin.ModelAdmin)
admin.site.register(Day, admin.ModelAdmin)
