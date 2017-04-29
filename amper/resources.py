from import_export import resources

from amper.models import Item


class ItemResource(resources.ModelResource):
    class Meta:
        model = Item
