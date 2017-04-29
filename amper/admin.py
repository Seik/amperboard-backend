from django.contrib import admin

from amper.models import Item

admin.site.register(Item, admin.ModelAdmin)
