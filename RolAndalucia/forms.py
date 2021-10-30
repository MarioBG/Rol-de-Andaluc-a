from django.core import exceptions
from django.forms import ModelForm, PasswordInput, forms, CharField,URLField, URLInput,Textarea,DateTimeField, ModelMultipleChoiceField,EmailInput, NumberInput, TextInput, MultipleChoiceField,EmailField, ModelMultipleChoiceField,CheckboxSelectMultiple, DateField, DateInput,SelectDateWidget,ChoiceField,RadioSelect,BooleanField, IntegerField
from django.contrib.auth.forms import UserCreationForm
from RolAndalucia.models import *
from django.contrib.auth.models import User, Group
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import datetime,timedelta
import django.contrib.auth.password_validation as validators
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


class UserForm(ModelForm):
    password = CharField(widget=PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')


class UserRegisterForm(forms.Form):

    def validate_inputEmail(data):
        email = data
        if User.objects.filter(email=email).exists():
            raise ValidationError({'inputEmail':["Ya existe un usuario con este email"]})

    def validate_password(self, pass1, pass2):
        errors = dict()
        if(pass1 != pass2):
            raise exceptions.ValidationError("Las contraseñas no coinciden")
        try:
            # validate the password and catch the exception
            validators.validate_password(password=pass1)
        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['inputPassword'] = list(e.messages)

        if errors:
            raise exceptions.ValidationError(errors)

    inputUsername = CharField(max_length=128, required=False, widget=TextInput(attrs={'placeholder': 'Nombre de usuario'}))
    inputEmail = CharField(max_length=256, required=False, widget=TextInput(attrs={'placeholder': 'Email'}), validators=[validate_inputEmail])
    inputPassword = CharField(max_length=256, required=False, widget=PasswordInput(attrs={'placeholder': 'Contraseña'}))
    inputPassword2 = CharField(max_length=256, required=False, widget=PasswordInput(attrs={'placeholder': 'Repite contraseña'}))

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        self.validate_password(cleaned_data.get("inputPassword"), cleaned_data.get("inputPassword2"))

    def save(self):
        u = User.objects.create(email=self.cleaned_data.get('inputEmail'), username=self.cleaned_data.get('inputUsername'))
        u.set_password(self.cleaned_data.get('inputPassword'))
        u.is_staff = True
        u.save()
        Group.objects.get(name="Usuario").user_set.add(u)


class UserProfileInfoForm(ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)