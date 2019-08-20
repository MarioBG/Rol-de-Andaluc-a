from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_list_or_404
from django.shortcuts import redirect
from django.views.generic import FormView, CreateView, UpdateView
from .models import *
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import datetime, timezone
from django.contrib import auth
from django.contrib import sessions
from django.contrib.auth.models import Group
from django.http import Http404,HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.db.models import Avg, Count, Min, Sum, Value, CharField, Aggregate
import random
from urllib.parse import urlparse, quote
from itertools import chain
import pytz
from django.utils import timezone

def index(request):
    # esto es como el controlador/servicios
    try:
        l = request.user.groups.values_list('name', flat=True)
        l_list = list(l)

    except:
        request.session['currentUser'] ='none'

    return render(request, 'index.html', {'spells':Spell.objects.all().count(), 'craftables':Craftable.objects.all().count(), 'items':Item.objects.all().count()})

def error404(request):
    return render(request, '404.html')