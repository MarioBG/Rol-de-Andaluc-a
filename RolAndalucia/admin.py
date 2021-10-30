import telegram
from django import db
from django.apps import apps
from django.contrib import admin
from django.utils.datetime_safe import datetime
from django_telegrambot.apps import DjangoTelegramBot

from RolAndalucia import models, views
from re import match, search
from RolAndalucia.models import DndAppointment
from django.db import transaction
from django.db.models import Q
from django.utils.html import format_html
from django.conf.urls import url
from django.utils.safestring import mark_safe
from admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, RangeNumericFilter, \
    SliderNumericFilter

from RolAndalucia.models import TelegramChat


def duplicate_event(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
    duplicate_event.short_description = "Duplicar registro"


class AddressInline(admin.StackedInline):
    model = models.PertenenciaClase
    extra = 0


class AppointmentDateInline(admin.StackedInline):
    model = models.DndAppointmentDate
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


class MensajeMovilInline(admin.StackedInline):
    model = models.MensajeMovil
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


class PjMadridAdmin(admin.ModelAdmin):
    list_filter = [
        'tags'
    ]


class ConversacionAdmin(admin.ModelAdmin):
    inlines = [MensajeMovilInline]
    list_filter = [
        'movil'
    ]


class CorreoMovilAdmin(admin.ModelAdmin):
    list_filter = [
        'movil'
    ]
    list_display = ['id', 'emisor', 'asunto', 'movil']
    list_display_links = ['emisor', 'asunto']
    search_fields = ['emisor', 'asunto']


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


class AppointmentAdmin(admin.ModelAdmin):

    def __init__(self, model, admin_site):
        self.request = None
        super().__init__(model, admin_site)

    def process_view(self, request, item_id, *args, **kwargs):
        print("To do") ##TODO Hacer el View de Appointment
        # return views.viewAppointment(request, item_id)

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

    def save_model(self, request, obj, form, change):
        with transaction.atomic():
            super(AppointmentAdmin, self).save_model(request, obj, form, change)
        dates = list()
        for e in form.data.keys():
            if bool(search("dates-\\d+-date_0", e) and e[:-6]+"DELETE" not in form.data):
                dates.append(datetime.strptime(form.data[e]+" "+form.data[e[:-1]+"1"], "%d/%m/%Y %H:%M:%S"))
        obj = DndAppointment.objects.get(id=obj.id)
        if not obj.dates.filter(confirmed=True):
            if (len(dates) > 0):
                message="📅*Actualización de planificación*📅\n\nLa sesión \"{}\", de la campaña {}, se ha " \
                        "actualizado con las siguientes posibles fechas.\n".format(obj.session_name, obj.campaign)
                for e in dates:
                    print(e)
                    message += "📅"+e.strftime("%d/%m/%Y,")+" ⌚"+e.strftime("%H:%M")+"\n"
                message += "¡Reserva plaza ahora en https://rol-andalucia.herokuapp.com/quedar/!"
            else:
                message = "📅*Actualización de planificación*📅\n\nLa sesión \"{}\", de la campaña {}, se ha " \
                          "creado y ahora está disponible para reservar en https://rol-andalucia.herokuapp.com/quedar/".format(form.cleaned_data.get("session_name"),
                                                                                     form.cleaned_data.get("campaign"))
            for chat in obj.chats.all():
                DjangoTelegramBot.bots[0].sendMessage(chat.groupId, message, parse_mode=telegram.ParseMode.MARKDOWN)
        db.connection.close()
        db.close_old_connections()

    inlines = [AppointmentDateInline]


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
    search_fields = ['name', 'effects', 'description']
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
admin.site.register(models.PjMadrid, PjMadridAdmin)
admin.site.register(models.CharacterClass, CharacterClassAdmin)
admin.site.register(models.Personaje, PersonajeAdmin)
admin.site.register(models.Spell, SpellAdmin)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.CorreoMovil, CorreoMovilAdmin)
admin.site.register(models.Conversacion, ConversacionAdmin)
admin.site.register(models.DndAppointment, AppointmentAdmin)

models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass