from django.forms import ModelForm, forms, CharField,URLField, URLInput,Textarea,DateTimeField, ModelMultipleChoiceField,EmailInput, NumberInput, TextInput, MultipleChoiceField,EmailField, ModelMultipleChoiceField,CheckboxSelectMultiple, DateField, DateInput,SelectDateWidget,ChoiceField,RadioSelect,BooleanField, IntegerField
from django.contrib.auth.forms import UserCreationForm
from RolAndalucia.models import *
from django.contrib.auth.models import User, Group
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import datetime,timedelta
import re
from django.contrib import admin

class SpellForm(ModelForm):

    class Meta:
        model = Spell
        fields = '__all__'

class CharacterClassForm(ModelForm):

    class Meta:
        model = CharacterClass
        fields= '__all__'


