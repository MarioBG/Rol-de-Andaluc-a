from django.contrib import sessions
from django.utils import translation
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from RolAndalucia.models import *


class GetLanguage(MiddlewareMixin):
    def process_request(self, request):
        if not request.session.has_key('_language'):
            request.session['_language'] = 'es-ES'
        language = request.session['_language']
        translation.activate(language)