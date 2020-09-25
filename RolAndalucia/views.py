from django.shortcuts import render, get_list_or_404
from .forms import *
from django.http import Http404,HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import template
from django.shortcuts import get_object_or_404, get_list_or_404
from RolAndalucia.models import *


def index(request):
    return render(request, 'index.html', {'spells':Spell.objects.all().count(), 'craftables':Craftable.objects.all().count(), 'items':Item.objects.all().count(), 'clases':CharacterClass.objects.all().count()})


def error404(request):
    return render(request, '404.html')


def login(request):
    return render(request, 'userAccount/login.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'dappx/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth.login(request, user)
                if request.method == 'POST' and 'next' in request.POST:
                    q = request.POST['next']
                    if q is not None and q != '':
                        return HttpResponseRedirect(q)
                    else:
                        return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return render(request, 'userAccount/login.html',
                          {'thing': "Credenciales incorrectas"})
    else:
        return render(request, 'userAccount/login.html', {})


def handler500(request, template_name="500.html"):
    return render(request, '500.html', status=500)


def handler404(request, atemplate_name="404.html"):
    return render(request, '404.html', status=404)


def viewItem(request):
    itemId = request.GET.get('itemId','')
    return render(request, 'displays/item.html', {'item':get_object_or_404(Item, pk = itemId)})


def viewClass(request):
    classId = request.GET.get('classId','')
    clase=CharacterClass.objects.get(pk=classId)
    if clase is not None:
        abilityDict=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        for ability in clase.habilidades.all():
            if ability.nivel <= 20:
                abilityDict[ability.nivel-1].append(ability)
    else:
        abilityDict={}
    return render(request, 'displays/class.html', {'clase':get_object_or_404(CharacterClass, pk=classId),
                                                   'abilityDict':abilityDict})


def viewCraftable(request):
    craftableId = request.GET.get('craftableId','')
    return render(request, 'displays/craftable.html', {'craftable':get_object_or_404(Craftable, pk = craftableId)})


def viewPersonaje(request):
    craftableId = request.GET.get('personajeId','')
    return render(request, 'displays/personaje.html', {'personaje':get_object_or_404(Personaje, pk = craftableId)})


def listPersonaje(request):
    return render(request, 'displays/personaje.html', {'personajes':Personaje.objects.all()})


def listTrabajo(request):
    return render(request, 'displays/trabajo.html', {'trabajos':Trabajo.objects.all()})


def viewWildemount(request):
    return render(request, 'displays/wildemount.html', {'trabajos':Trabajo.objects.all()})


def viewTrabajo(request):
    craftableId = request.GET.get('trabajoId','')
    return render(request, 'displays/trabajo.html', {'trabajo':get_object_or_404(Trabajo, pk = craftableId)})

def searchEntryName(request):
    name = request.GET.get('q','')
    name = name.replace("_"," ")
    motes = name.split(">")
    if motes and type(motes)=='list' and len(motes) > 1:
        if motes[0].lower() == "s":
            return render(request, 'displays/spell.html', {'spell': get_object_or_404(Spell, name=motes[1])})
        elif motes[0].lower() == "i":
            return render(request, 'displays/item.html', {'item': get_object_or_404(Item, name=motes[1])})
        elif motes[0].lower() == "c":
            return render(request, 'displays/class.html', {'clase': get_object_or_404(CharacterClass, name=motes[1])})
        elif motes[0].lower() == "m":
            return render(request, 'displays/craftable.html', {'craftable': get_object_or_404(Craftable, name=motes[1])})
    item = Item.objects.filter(name=name).first()
    craftable = Craftable.objects.filter(name=name).first()
    clase = CharacterClass.objects.filter(name=name).first()
    spell = Spell.objects.filter(name=name).first()
    if spell is not None:
        return render(request, 'displays/spell.html', {'spell': spell})
    elif clase is not None:
        return render(request, 'displays/class.html', {'clase': clase})
    elif craftable is not None:
        return render(request, 'displays/craftable.html', {'craftable': craftable})
    elif item is not None:
        return render(request, 'displays/item.html', {'item': item})


def viewSpell(request):
    spellId = request.GET.get('spellId', '')
    return render(request, 'displays/spell.html', {'spell': get_object_or_404(Spell, pk = spellId), })