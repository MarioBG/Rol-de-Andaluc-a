"""RolAndalucia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from rest_framework import routers
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

handler404 = "RolAndalucia.views.handler404"
handler500 = "RolAndalucia.views.handler500"

router = routers.DefaultRouter()

admin.autodiscover()
admin.site.login = views.login
admin.site.logout = views.user_logout

urlpatterns = [
    path('admin/login/', views.login),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('logout', views.user_logout, name='logout'),
    path('login', views.login, name='login'),
    path('doLogin', views.user_login, name='doLogin'),
    path('viewItem', views.viewItem, name='viewItem'),
    path('viewSpell', views.viewSpell, name='viewSpell'),
    path('viewPersonaje', views.viewPersonaje, name='viewPersonaje'),
    path('listPersonaje', views.listPersonaje, name='listPersonaje'),
    path('wildemount', views.viewWildemount, name='wildemount'),
    path('cds', views.viewCds, name='cds'),
    path('diario', views.viewDiario, name='diario'),
    path('viewTrabajo', views.viewTrabajo, name='viewTrabajo'),
    path('listTrabajo', views.listTrabajo, name='listTrabajo'),
    path('viewCraftable', views.viewCraftable, name='viewCraftable'),
    path('404', views.error404, name='404'),
    path('500', views.handler500, name='500'),
    path('searchName', views.searchEntryName, name='searchName'),
    path('viewClass', views.viewClass, name='viewClass'),
    path('martor/', include('martor.urls')),
    url(r'^treewidget/', include('treewidget.urls')),
    url(r'^movilInfo/(?P<uid>[-\d]+)/', views.movilInfo.as_view(), name = 'movilInfo'),
]