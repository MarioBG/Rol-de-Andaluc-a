from django.contrib.auth.models import User, Group
from requests import request
from rest_framework import serializers
from RolAndalucia.models import *
from rest_framework.validators import UniqueValidator
from rest_framework.permissions import *
import django.contrib.auth.password_validation as validators
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.template import Context, loader
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth.models import Permission
from django.db import transaction
from django import db

class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = ['titular', 'subtitulo']


class MensajeMovilSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeMovil
        fields = ['texto', 'mio']


class CalendarioJsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarioJson
        fields = ['content']


class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foto
        fields = ['lowRes', 'hiRes']


class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = ['dia', 'titulo', 'subtitulo']


class CorreoMovilSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorreoMovil
        fields = ['emisor', 'asunto', 'cuerpo']


class LlamadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Llamada
        fields = ['numero', 'hora', 'tipo']


class ConversacionSerializer(serializers.ModelSerializer):
    mensajeMovils = MensajeMovilSerializer(many=True)
    class Meta:
        model = Conversacion
        fields = ['destinatario', 'mensajeMovils']


class MovilSerializer(serializers.ModelSerializer):
    conversacions = ConversacionSerializer(many=True)
    noticias = NoticiaSerializer(many=True)
    correoMovils = CorreoMovilSerializer(many=True)
    fotos = FotoSerializer(many=True)
    notas = NotaSerializer(many=True)
    llamadas = LlamadaSerializer(many=True)
    calendarioJson = CalendarioJsonSerializer()
    class Meta:
        model = Movil
        fields = ['nombreDueno', 'modelo', 'fecha', 'colorAcento', 'conversacions', 'noticias', 'correoMovils',
                  'fotos', 'notas', 'llamadas', 'calendarioJson']