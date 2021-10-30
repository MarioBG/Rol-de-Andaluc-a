import telegram
from colorfield.fields import ColorField
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django_telegrambot.apps import DjangoTelegramBot
from martor.models import MartorField
import django.core.validators
from ordered_model.models import OrderedModel
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel
import mptt
from django.db.models import F
from treewidget.fields import TreeForeignKey
from django_imgur.storage import ImgurStorage

# Create your models here.
# System objects

STORAGE = ImgurStorage()


class Rule(MPTTModel):
    
    name = models.CharField(verbose_name=_("Nombre"), max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    content = MartorField(verbose_name=_("Content"), default='')
    order = models.PositiveIntegerField(verbose_name=_("Orden"), default=0)
    order_with_respect_to = 'parent'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if Rule.objects.filter(order__gte = self.order):
            Rule.objects.filter(order__gte =self.order, parent = self.parent).update(order=F('order') + 1)
        super(Rule, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Rule, self).delete(*args, **kwargs)


class TagPjMadrid(models.Model):
    name = models.CharField(verbose_name=_("Nombre de etiqueta"), max_length=50)
    key = models.CharField(verbose_name=_("Valor de etiqueta"), max_length=16)
    def __str__(self):
        return self.name


class PjMadrid(models.Model):
    pic = models.ImageField(upload_to='profile_pics', null=True, blank=True, storage=STORAGE)
    name = models.CharField(verbose_name=_("Nombre"), max_length=100)
    position = models.CharField(verbose_name=_("Trabajo"), max_length=200)
    description = models.TextField(verbose_name=_("Descripción"))
    jugador = models.CharField(verbose_name=_("Jugador"), max_length=30, null=True, blank=True)
    tags = models.ManyToManyField(to=TagPjMadrid, verbose_name=_("Tags"), related_name="pjs")
    def __str__(self):
        return self.name


class CharacterClass(models.Model):

    name = models.TextField(verbose_name=_("Nombre de clase"))
    description = MartorField(verbose_name=_("Descripción"), default='')

    def __str__(self):
        return self.name


class TelegramChat(models.Model):
    name = models.CharField(verbose_name=_("Nombre del chat"), max_length=280)
    groupId = models.CharField(verbose_name=_("ID del grupo"), max_length=64, blank=False, null=False)

    def __str__(self):
        return self.name


class DndAppointment(models.Model):
    CHOICES=[("P", "presencial"), ("O", "online")]
    pic = models.ImageField(upload_to='session_pics', null=True, blank=True, storage=STORAGE)
    campaign = models.TextField(verbose_name=_("Campaña"))
    tipo = models.CharField(verbose_name=_("Tipo de sesión"), choices=CHOICES, max_length=2, null=False)
    location = models.CharField(verbose_name=_("Ubicación"), max_length=72, null=True)
    session_name = models.TextField(verbose_name=_("Nombre de sesión"))
    chats = models.ManyToManyField(verbose_name=_("Chats para anunciar"), to=TelegramChat)

    def getConfirmedAppointment(self):
        return self.dates.filter(confirmed=True).first()

    def save(self):
            super(DndAppointment, self).save()
            message = ""
            for e in self.dates.all():
                if e.confirmed == True:
                    message += "📅*Actualización de planificación*📅\n\nLa sesión \"{}\", de la campaña {}, se ha " \
                              "confirmado para el {} a las {}.\n\n*ASISTENTES:*\n".format(self.session_name,
                                                                                        self.campaign,
                                                                                        e.date.strftime("%d/%m/%Y"),
                                                                                        e.date.strftime("%H:%M"))
                    for i in e.reservations.filter(type__exact="YES"):
                        message += "✅ {}\n".format(i.user.username)
                    if e.reservations.filter(type__exact="IF_NEED"):
                        message += "\n*POR CONFIRMAR:*\n"
                        for i in e.reservations.filter(type__exact="IF_NEED"):
                            message += "❔ {}\n".format(i.user.username)
                    for chat in self.chats.all():
                        DjangoTelegramBot.bots[0].sendMessage(chat.groupId, message, parse_mode=telegram.ParseMode.MARKDOWN)
                    break

    def __str__(self):
        return self.session_name


class DndAppointmentDate(models.Model):
    appointment = models.ForeignKey(to=DndAppointment, related_name="dates", on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name=_("Fecha y hora"), null=False)
    confirmed = models.BooleanField(verbose_name=_("Fecha confirmada"), null=False)

    def __str__(self):
        return self.appointment.session_name+" ("+self.date.strftime("%d/%m/%Y, %H:%M")+")"


    def clean(self):
        if (len(self.appointment.dates.filter(confirmed=True)) > 0 and self.appointment.dates.get(confirmed=True).pk is not self.pk and self.confirmed == True):
            raise ValidationError({"confirmed": "No puede haber más de una fecha confirmada para cada appointment"})


class DndRsvp(models.Model):
    CHOICES = [('YES', 'Confirmo asistencia'), ('IF_NEED', 'Solo si es necesario')]

    dndAppointment = models.ForeignKey(to=DndAppointmentDate, related_name="reservations", on_delete=models.CASCADE)
    type = models.CharField(verbose_name=_("Tipo de reserva"), max_length=30, blank=False, choices=CHOICES)
    user = models.ForeignKey(to=User, related_name="reservations", on_delete=models.CASCADE)



class Spell(models.Model):

    CHOICES=[('Abjuración', 'Abjuración'),('Conjuración', 'Conjuración'),('Adivinación', 'Adivinación'),
             ('Encantamiento', 'Encantamiento'),('Evocación', 'Evocación'),('Ilusión', 'Ilusión'),
             ('Nigromancia', 'Nigromancia'),('Transmutación', 'Transmutación')]

    class Meta():
        ordering=["level", "school", "name"]

    name = models.CharField(verbose_name=_("Spell name"), max_length=50, blank=False)
    school = models.CharField(verbose_name=_("School of Magic"), max_length=30, blank=False, choices=CHOICES)
    level = models.PositiveIntegerField(verbose_name=_("Spell level"), null=False)
    verbalComponent = models.BooleanField(verbose_name=_("Verbal Component"), default=False)
    somaticComponent = models.BooleanField(verbose_name=_("Somatic Component"), default=False)
    materialComponent = models.BooleanField(verbose_name=_("Material Component"), default=False)
    materialRequirements = models.CharField(verbose_name=_("Material requirements"), max_length=200, blank=True)
    castTime = models.CharField(verbose_name=_("Casting time"), max_length=100, default="N/A")
    duration = models.CharField(verbose_name=_("Duration"), max_length=100, default="N/A")
    concentration = models.BooleanField(verbose_name=_("Concentration"), default=False)
    range = models.CharField(verbose_name=_("Range/Area"), max_length=100, default="N/A")
    effect = models.CharField(verbose_name=_("Damage/effect type"), max_length=100, default="N/A")
    attack_save = models.CharField(verbose_name=_("Attack or save"), max_length=100, default="N/A")
    description = models.TextField(verbose_name=_("Description"), default="")
    classes = models.ManyToManyField(to=CharacterClass, verbose_name=_("Classes that use this spell"))

    def __str__(self):
        return self.name+" (Nv"+str(self.level)+", "+self.school+")"


class Craftable(models.Model):

    name = models.CharField(verbose_name=_("Nombre de creación"), max_length=50, blank=False)
    description = models.TextField(verbose_name=_("Descripción"))
    programmingCost = models.PositiveIntegerField(verbose_name=_("Coste de programación"))
    engineeringCost = models.PositiveIntegerField(verbose_name=_("Coste de ingeniería"))
    scientificCost = models.PositiveIntegerField(verbose_name=_("Coste científico"), default = 0)
    materialCost = models.TextField(verbose_name=_("Costes en materiales"), blank=True)
    effect = models.TextField(verbose_name=_("Efectos"))
    requirements = models.TextField(verbose_name=_("Requisitos"), blank=True)
    photo = models.CharField(verbose_name=_("Imagen"), blank=True, max_length=400)
    vehicular = models.BooleanField(verbose_name=_("Para coche"), default=False)
    biological = models.BooleanField(verbose_name=_("Biológico"), default=False)
    application = models.BooleanField(verbose_name=_("Aplicación"), default=False)
    artifact = models.BooleanField(verbose_name=_("Artefacto"), default=False)

    def __str__(self):
        return self.name


class Item(models.Model):

    name = models.CharField(verbose_name=_("Nombre de objeto"), max_length=60, blank=False)
    description = models.TextField(verbose_name=_("Descripción"))
    type = models.CharField(verbose_name=_("Tipo de objeto"), max_length=30)
    rarity = models.CharField(verbose_name=_("Rareza"), max_length=20, blank=True)
    notes = models.CharField(verbose_name=_("Notas"), max_length=100, blank=True)
    magic = models.BooleanField(verbose_name=_("Magia"), default=False)
    wearable = models.BooleanField(verbose_name=_("Equipable"), default=False)
    effects = models.TextField(verbose_name=_("Efectos"), blank=True)
    characteristics = models.TextField(verbose_name=_("Características"), blank=True, help_text="Genera tablas en https://www.tablesgenerator.com/markdown_tables#")
    photo = models.CharField(verbose_name=_("Imagen"), blank=True, max_length=400)

    def __str__(self):
        return self.name


class StatBlock(models.Model):

    strength = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)], default=10)
    dexterity = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)], default=10)
    constitution = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)], default=10)
    intelligence = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)], default=10)
    wisdom = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)], default=10)
    charisma = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)], default=10)
    proficiencyBonus = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)], default=10)

    def __str__(self):
        try:
            return "Bloque de stats de "+self.personaje.name
        except ObjectDoesNotExist:
            return "¡Guarda el personaje!"


class Score(models.Model):
    statBlock=models.ForeignKey(to=StatBlock, on_delete=models.CASCADE, related_name="scores")
    address = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    enabled = models.BooleanField(default=False)


class Personaje(models.Model):

    def save(self, *args, **kwargs):
        if not self.pk and self.statBlock is None:
            self.statBlock = StatBlock()
        super(Personaje, self).save(*args, **kwargs)

    name = models.CharField(verbose_name=_("Nombre de personaje"), max_length=60, blank=False)
    hechizos = models.ManyToManyField(to=Spell, verbose_name=_("Hechizos"), blank=True)
    maxHp = models.IntegerField(verbose_name=_("Salud máxima"), validators=[MinValueValidator(limit_value=0)])
    temporaryHp = models.IntegerField(verbose_name=_("Salud máxima"), validators=[MinValueValidator(limit_value=0)], null=True)
    currentHp = models.IntegerField(verbose_name=_("Salud actual"), validators=[MinValueValidator(limit_value=0)])
    armorClass = models.IntegerField(verbose_name=_("Clase de armadura"), validators=[MinValueValidator(limit_value=0)], null=True)
    habilidades = MartorField(verbose_name=_("Habilidades"), default='', blank=True)
    descripcion = MartorField(verbose_name=_("Habilidades"), default='', blank=True)
    photo = models.CharField(verbose_name=_("Imagen"), blank=True, max_length=400)
    jugador = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    inspiration = models.BooleanField(default=False)
    statBlock = models.OneToOneField(to=StatBlock, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class InventoryEntry(models.Model):

    item = models.ForeignKey(to=Item, on_delete=models.CASCADE, null=True)
    personaje = models.ForeignKey(to=Personaje, on_delete=models.CASCADE, related_name="inventoryEntries")
    count = models.DecimalField(default=1, decimal_places=2, max_digits=12)
    unit = models.CharField(null=True, max_length=20)
    name = models.CharField(verbose_name=_("Nombre de objeto"), max_length=60, null=True)
    descripcion = MartorField(verbose_name=_("Descripción"), null=True)

    def __str__(self):
        return self.item.name+" ("+self.count+self.unit+")"


class Trabajo(models.Model):

    name = models.CharField(verbose_name=_("Nombre de trabajo"), max_length=60, blank=False)
    empleador = models.CharField(verbose_name=_("Empleador"), blank=True, max_length=400)
    salario = models.IntegerField(verbose_name=_("Salario ofrecido"), validators=[MinValueValidator(limit_value=0)])
    descripcion = MartorField(verbose_name=_("Descripción"), default='')
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CalendarioJson(models.Model):
    content = models.CharField(blank=False, max_length=131072)


class Movil(models.Model):
    nombreDueno = models.CharField(verbose_name=_("Dueño"), blank=False, max_length=60)
    modelo = models.CharField(verbose_name=_("Modelo"), blank=False, max_length=60)
    fecha = models.DateTimeField()
    colorAcento = ColorField(default="#5B7DB3")
    calendarioJson = models.ForeignKey(to=CalendarioJson, on_delete=models.PROTECT)

    def __str__(self):
        return self.modelo+" de "+self.nombreDueno


class Noticia(models.Model):
    titular = models.CharField(verbose_name=_("Titular"), blank=False, max_length=240)
    subtitulo = models.TextField(verbose_name=_("Subítulo"), blank=False, max_length=1024)
    movil = models.ForeignKey(to=Movil, on_delete=models.CASCADE, null=False, related_name="noticias")

    def __str__(self):
        return self.titular


class Llamada(models.Model):
    CHOICES=[('REC', 'Recibida'), ('ENV', 'Enviada'), ('PER', 'Perdida')]
    numero = models.CharField(verbose_name=_("Numero"), blank=False, max_length=32)
    hora = models.CharField(verbose_name=_("Hora"), blank=False, max_length=32)
    tipo = models.CharField(verbose_name=_("Hora"), blank=False, max_length=8, choices=CHOICES)
    movil = models.ForeignKey(to=Movil, on_delete=models.CASCADE, null=False, related_name="llamadas")

    def __str__(self):
        return self.numero+" ("+str(self.movil)+")"


class Nota(models.Model):
    dia = models.DateField()
    titulo = models.CharField(verbose_name=_("Titulo"), blank=False, max_length=240)
    subtitulo = models.TextField(verbose_name=_("Subítulo"), blank=False, max_length=480)
    movil = models.ForeignKey(to=Movil, on_delete=models.CASCADE, null=False, related_name="notas")

    def __str__(self):
        return self.titulo


class Conversacion(models.Model):
    destinatario = models.CharField(verbose_name=_("Destinatario"), blank=False, max_length=240)
    movil = models.ForeignKey(to=Movil, on_delete=models.CASCADE, null=False, related_name="conversacions")

    def __str__(self):
        return self.destinatario+" desde "+str(self.movil)


class MensajeMovil(models.Model):
    mio = models.BooleanField(blank=False)
    texto = models.TextField(max_length=2048, blank=False)
    conversacion = models.ForeignKey(to=Conversacion, on_delete=models.CASCADE, null=False, related_name="mensajeMovils")

    def __str__(self):
        return self.texto[:24]


class CorreoMovil(models.Model):
    emisor = models.CharField(verbose_name=_("Emisor"), blank=False, max_length=240)
    asunto = models.CharField(verbose_name=_("Asunto"), blank=False, max_length=240)
    cuerpo = models.TextField(verbose_name=_("Cuerpo"), blank=False, max_length=2048)
    movil = models.ForeignKey(to=Movil, on_delete=models.CASCADE, null=False, related_name="correoMovils")

    def __str__(self):
        return self.asunto+" ("+self.emisor+")"


class Foto(models.Model):
    desc = models.CharField(verbose_name=_("Asunto"), blank=True, max_length=32)
    lowRes = models.CharField(verbose_name=_("Baja resolución"), blank=False, max_length=240)
    hiRes = models.CharField(verbose_name=_("Alta resolución"), blank=False, max_length=240)
    movil = models.ForeignKey(to=Movil, on_delete=models.CASCADE, null=False, related_name="fotos")

    def __str__(self):
        return self.desc


class PertenenciaClase(models.Model):

    personaje = models.ForeignKey(to=Personaje, related_name='pertenenciasClase', on_delete=models.CASCADE)
    clase = models.ForeignKey(to=CharacterClass, on_delete=models.CASCADE)
    nivel = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)

    def __str__(self):
        try:
            return "Clase de "+self.personaje.name
        except ObjectDoesNotExist:
            return "¡Guarda el personaje!"


class Ability(models.Model):
    clase = models.ForeignKey(to=CharacterClass, related_name='habilidades', on_delete=models.CASCADE)
    nombre = models.CharField(verbose_name=_("Nombre de habilidad"), blank=False, max_length=120)
    descripcion = MartorField(verbose_name=_("Descripción"),default=_("Esta habilidad no tiene descripción"))
    nivel = models.IntegerField(verbose_name=_("Nivel"))
    desbloqueo = MartorField(verbose_name=_("Condiciones de desbloqueo"), default="N/A")
    isOptional = models.BooleanField(verbose_name=_("Habilidad opcional"), default=False)
    expCost = models.IntegerField(verbose_name=_("Coste en experiencia"), default=0)

    def __str__(self):
        return self.nombre


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    def __str__(self):
      return self.user.username



# class GameMaster(models.Model):
#
# class Player(models.Model):
#
#
# class Party(models.Model):
#
#
# class Campaign(models.Model):
