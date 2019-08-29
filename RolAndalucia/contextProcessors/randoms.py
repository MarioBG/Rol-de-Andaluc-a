from django.shortcuts import render, get_list_or_404
from RolAndalucia.forms import *
from django.http import Http404,HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def randoms(request):
    result = {}
    result['randItem'] = Item.objects.order_by("?").first()
    result['randCraftable'] = Craftable.objects.order_by("?").first()
    result['randSpell'] = Spell.objects.order_by("?").first()
    result['classes'] = CharacterClass.objects.all()
    return result
