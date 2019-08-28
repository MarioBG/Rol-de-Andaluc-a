from django.apps import apps
from django.contrib import admin
from RolAndalucia import models, views
from django.db.models import Q
from django.utils.html import format_html
from django.conf.urls import url
from django.utils.safestring import mark_safe
from admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, RangeNumericFilter, \
    SliderNumericFilter


def duplicate_event(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
duplicate_event.short_description = "Duplicar registro"

class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)


class SpellAdmin(NumericFilterModelAdmin):
    list_display = ('id', 'name', 'level', 'school', 'castTime', 'duration', 'concentration', 'effect')
    list_display_links = ('name', 'id')
    search_fields = ['name', 'school', 'effect']
    actions = [duplicate_event]
    list_per_page = 25
    list_filter = [["level", RangeNumericFilter],"school","classes", "verbalComponent", "somaticComponent", "materialComponent","concentration"]


class CraftableAdmin(NumericFilterModelAdmin):
    list_display = ('id', 'name', 'programmingCost', 'engineeringCost', 'description')
    list_display_links = ('name', 'id')
    search_fields = ['name', 'effect']
    actions = [duplicate_event]
    list_per_page = 25
    list_filter = [
        ['programmingCost', SliderNumericFilter],
        ['engineeringCost', SliderNumericFilter]
    ]

class ItemAdmin(admin.ModelAdmin):

    def __init__(self, model, admin_site):
        self.request = None
        super().__init__(model, admin_site)

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

    list_display = ('item_actions','id', 'name', 'type', 'magic', 'wearable', 'rarity' )
    list_display_links = []
    search_fields = ['name', 'effect', 'description']
    list_per_page = 25
    actions = [duplicate_event]
    list_filter = [
        'magic', 'wearable', 'type', 'rarity'
    ]

    def vacio(self, obj):
        return ''

    def process_view(self, request, item_id, *args, **kwargs):
        return views.viewItem(request, item_id)


    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         url(
    #             r'^(?P<item_id>.+)/view/$',
    #             self.admin_site.admin_view(self.process_view),
    #             name='item-view',
    #         ),
    #     ]
    #     return custom_urls + urls

    def item_actions(self, obj):
        ans = '<a class="button" href="/viewItem?itemId='+str(obj.pk)+'">Ver</a>&nbsp;'
        if self.request.user.groups.filter(name="Admin").exists():
            ans += '</a><a class="button" href="/admin/RolAndalucia/item/'+str(obj.pk)+'/change">Editar</a>&nbsp;'
        return mark_safe(ans)

    item_actions.short_description = 'Acciones'
    item_actions.allow_tags = True


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