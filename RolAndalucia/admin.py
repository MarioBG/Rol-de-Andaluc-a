from django.apps import apps
from django.contrib import admin
from RolAndalucia import models
from django.db.models import Q
from admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, RangeNumericFilter, \
    SliderNumericFilter


class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)


class SpellAdmin(NumericFilterModelAdmin):
    list_display = ('id', 'name', 'level', 'school', 'castTime', 'duration', 'concentration', 'effect')
    list_display_links = ('name', 'id')
    search_fields = ['name', 'school', 'effect']
    list_per_page = 25
    list_filter = [["level", RangeNumericFilter],"school","classes", "verbalComponent", "somaticComponent", "materialComponent","concentration"]


class CraftableAdmin(NumericFilterModelAdmin):
    list_display = ('id', 'name', 'programmingCost', 'engineeringCost', 'description')
    list_display_links = ('name', 'id')
    search_fields = ['name', 'effect']
    list_per_page = 25
    list_filter = [
        ['programmingCost', SliderNumericFilter],
        ['engineeringCost', SliderNumericFilter]
    ]

class ItemAdmin(NumericFilterModelAdmin):
    list_display = ('id', 'name', 'type', 'magic', 'wearable', 'rarity')
    list_display_links = ('name', 'id')
    search_fields = ['name', 'effect', 'description']
    list_per_page = 25
    list_filter = [
        'magic', 'wearable', 'type', 'rarity'
    ]



admin.site.register(models.Craftable, CraftableAdmin)
admin.site.register(models.Spell, SpellAdmin)
admin.site.register(models.Item, ItemAdmin)

models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass