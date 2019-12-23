from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from martor.models import MartorField
import django.core.validators
from ordered_model.models import OrderedModel
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel
import mptt
from django.db.models import F
from treewidget.fields import TreeForeignKey

# Create your models here.
# System objects


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


class CharacterClass(models.Model):

    name = models.TextField(verbose_name=_("Nombre de clase"))
    description = MartorField(verbose_name=_("Descripción"), default='')

    def __str__(self):
        return self.name


class Spell(models.Model):

    class Meta():
        ordering=["level", "school", "name"]

    name = models.CharField(verbose_name=_("Spell name"), max_length=50, blank=False)
    school = models.CharField(verbose_name=_("School of Magic"), max_length=30, blank=False)
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


class InventoryEntry(models.Model):

    item = models.ForeignKey(to=Item, on_delete=models.CASCADE, null=True)
    personaje = models.ForeignKey(to=Personaje, on_delete=models.CASCADE, related_name="inventoryEntries")
    count = models.DecimalField(default=1, decimal_places=2, max_digits=12)
    unit = models.CharField(null=True, max_length=20)
    name = models.CharField(verbose_name=_("Nombre de objeto"), max_length=60, null=True)
    descripcion = MartorField(verbose_name=_("Descripción"), null=True)


class Trabajo(models.Model):

    name = models.CharField(verbose_name=_("Nombre de trabajo"), max_length=60, blank=False)
    empleador = models.CharField(verbose_name=_("Empleador"), blank=True, max_length=400)
    salario = models.IntegerField(verbose_name=_("Salario ofrecido"), validators=[MinValueValidator(limit_value=0)])
    descripcion = MartorField(verbose_name=_("Descripción"), default='')
    visible = models.BooleanField(default=False)


class PertenenciaClase(models.Model):

    personaje = models.ForeignKey(to=Personaje, related_name='pertenenciasClase', on_delete=models.CASCADE)
    clase = models.ForeignKey(to=CharacterClass, on_delete=models.CASCADE)
    nivel = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)


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
