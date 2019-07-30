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