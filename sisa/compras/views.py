from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.template import context

from .forms import *
from django.apps import AppConfig
from django.apps import AppConfig

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

con1=1

# Create your views here.
def infrendprov(request):
    if request.user.is_authenticated:
        return render(request, "informeprov/infrendprov.html")
    else:
        return redirect('login')


def menucompras(request):
    if request.user.is_authenticated:
        return render(request, 'compras/menucompras.html')
    else:
        return redirect('login')

def menuproveedor(request):
    if request.user.is_authenticated:
        return render(request, 'compras/menuproveedor.html')
    else:
        return redirect('login')

