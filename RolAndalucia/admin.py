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


class AddressInline(admin.StackedInline):
    model = models.PertenenciaClase
    extra = 0


class ScoreInline(admin.StackedInline):
    model = models.Score
    extra = 0


class StatBlockInline(admin.StackedInline):
    model = models.StatBlock
    extra = 0


class AbilityInline(admin.StackedInline):
    model = models.Ability
    extra = 0



class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)


class SpellAdmin(NumericFilterModelAdmin):
    def __init__(self, model, admin_site):
        self.request = None
        super().__init__(model, admin_site)

    def process_view(self, request, item_id, *args, **kwargs):
        return views.viewItem(request, item_id)

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

    list_display = ('spell_actions', 'id', 'name', 'level', 'school', 'castTime', 'duration', 'concentration', 'effect')
    search_fields = ['name', 'school', 'effect']
    actions = [duplicate_event]
    list_per_page = 25
    list_filter = [["level", RangeNumericFilter],"school","classes", "verbalComponent", "somaticComponent", "materialComponent","concentration"]

    def spell_actions(self, obj):
        ans = '</a><a class="button" href="/viewSpell?spellId='+str(obj.pk)+'">Ver</a>&nbsp;'
        if self.request.user.groups.filter(name="Admin").exists():
            ans += '<a class="button" href="/admin/RolAndalucia/spell/'+str(obj.pk)+'/change">Editar</a>&nbsp;'
        return mark_safe(ans)

    spell_actions.short_description = 'Acciones'
    spell_actions.allow_tags = True


class StatBlockAdmin(admin.ModelAdmin):
    inlines = [ScoreInline]


class PersonajeAdmin(admin.ModelAdmin):

    def __init__(self, model, admin_site):
        self.request = None
        super().__init__(model, admin_site)

    def process_view(self, request, item_id, *args, **kwargs):
        return views.viewPersonaje(request, item_id)

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

    list_display = ['spell_actions', 'name', 'currentHp']
    inlines = [AddressInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'hechizos', 'maxHp', 'currentHp', 'photo', 'jugador', 'statBlock')
        }),
        ('Habilidades', {
            'classes': ('collapse',),
            'fields': ('habilidades',),
        }),
        ('Descripción', {
            'classes': ('collapse',),
            'fields': ('descripcion',),
        }),
    )

    def spell_actions(self, obj):
        ans = '</a><a class="button" href="/viewPersonaje?personajeId='+str(obj.pk)+'">Ver</a>&nbsp;'
        if self.request.user.groups.filter(name="Admin").exists():
            ans += '<a class="button" href="/admin/RolAndalucia/personaje/'+str(obj.pk)+'/change">Editar</a>&nbsp;'
        return mark_safe(ans)
    list_per_page = 25

    spell_actions.short_description = 'Acciones'
    spell_actions.allow_tags = True


class CharacterClassAdmin(NumericFilterModelAdmin):
    def __init__(self, model, admin_site):
        self.request = None
        super().__init__(model, admin_site)

    def process_view(self, request, item_id, *args, **kwargs):
        return views.viewItem(request, item_id)

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

    list_display = ('class_actions', 'id', 'name')
    search_fields = ['name']
    inlines = [AbilityInline]
    actions = [duplicate_event]
    list_per_page = 25

    def class_actions(self, obj):
        ans = '</a><a class="button" href="/viewClass?classId='+str(obj.pk)+'">Ver</a>&nbsp;'
        if self.request.user.groups.filter(name="Admin").exists():
            ans += '<a class="button" href="/admin/RolAndalucia/characterclass/'+str(obj.pk)+'/change">Editar</a>&nbsp;'
        return mark_safe(ans)

    class_actions.short_description = 'Acciones'
    class_actions.allow_tags = True


class CraftableAdmin(NumericFilterModelAdmin):

    def __init__(self, model, admin_site):
        self.request = None
        super().__init__(model, admin_site)

    def process_view(self, request, item_id, *args, **kwargs):
        return views.viewItem(request, item_id)

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

    list_display = ('craftable_actions', 'id', 'name', 'programmingCost', 'engineeringCost', 'description')
    search_fields = ['name', 'effect']
    actions = [duplicate_event]
    list_per_page = 25
    list_filter = [
        ['programmingCost', SliderNumericFilter],
        ['engineeringCost', SliderNumericFilter], 'vehicular', 'biological', 'application', 'artifact'
    ]

    def craftable_actions(self, obj):
        ans = '</a><a class="button" href="/viewCraftable?craftableId='+str(obj.pk)+'">Ver</a>&nbsp;'
        if self.request.user.groups.filter(name="Admin").exists():
            ans += '<a class="button" href="/admin/RolAndalucia/craftable/'+str(obj.pk)+'/change">Editar</a>&nbsp;'
        return mark_safe(ans)

    craftable_actions.short_description = 'Acciones'
    craftable_actions.allow_tags = True

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
admin.site.register(models.CharacterClass, CharacterClassAdmin)
admin.site.register(models.Personaje, PersonajeAdmin)
admin.site.register(models.Spell, SpellAdmin)
admin.site.register(models.Item, ItemAdmin)

models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass