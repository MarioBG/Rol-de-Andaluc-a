from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# Create your models here.
# System objects


class Configuration(models.Model):
    threadPrice = models.IntegerField(verbose_name=_("Thread Price"), null=False, default=0)
    jobOfferPrice = models.IntegerField(verbose_name=_("Job Offer Price"), null= False, default=0)
    challengePrice = models.IntegerField(verbose_name=_("Challenge Price"), null=False, default=0)
    defaultMaxCoins = models.IntegerField(verbose_name=_("Default maximum coins"), null=False, default=10)
    directPurchaseCoinsPrice = models.FloatField(verbose_name=_("Coins price"), null=False, default=3)


class CharacterClass(models.Model):
    name = models.TextField(verbose_name="Class name")

    def __str__(self):
        return self.name

class Spell(models.Model):
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
        return self.name


class Craftable(models.Model):
    name = models.CharField(verbose_name=_("Nombre de creación"), max_length=50, blank=False)
    description = models.TextField(verbose_name=_("Descripción"))
    programmingCost = models.PositiveIntegerField(verbose_name=_("Coste de programación"))
    engineeringCost = models.PositiveIntegerField(verbose_name=_("Coste de ingeniería"))
    materialCost = models.TextField(verbose_name=_("Costes en materiales"), blank=True)
    effect = models.TextField(verbose_name=_("Efectos"))
    requirements = models.TextField(verbose_name=_("Requisitos"), blank=True)
    photo = models.URLField(verbose_name=_("Imagen"), blank=True)

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
    photo = models.URLField(verbose_name=_("Imagen"), blank=True)

    def __str__(self):
        return self.name



# class GameMaster(models.Model):
#
# class Player(models.Model):
#
#
# class Party(models.Model):
#
#
# class Campaign(models.Model):
