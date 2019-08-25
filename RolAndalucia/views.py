from django.shortcuts import render, get_list_or_404
from .forms import *
from django.http import Http404,HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import template

def index(request):
    return render(request, 'index.html', {'spells':Spell.objects.all().count(), 'craftables':Craftable.objects.all().count(), 'items':Item.objects.all().count()})

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


def handler500(request, exception, template_name="500.html"):
    return render(request, '500.html', status=500)


def handler404(request, exception, template_name="404.html"):
    return render(request, '404.html', status=404)


def viewItem(request):
    itemId = request.GET.get('itemId','')
    item = Item.objects.get(pk = itemId)
    return render(request, 'displays/item.html', {'item':item,})
