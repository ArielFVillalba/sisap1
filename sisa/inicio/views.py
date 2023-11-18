from django.contrib.auth.models import User
from django.db import connections, connection
from django.http import JsonResponse, response
from django.shortcuts import render
from inicio.funcion import *
import http.cookiejar
import urllib.request

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required


app_name = 'inicio'
con1=1;
# Create your views here.

def error_404(request, exception):
    return redirect('login')
def error(request):
    return redirect('login')

def loginc(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            user_permissions = user.user_permissions.all()
            valor=str(user.last_login)+str(user.username)+str(user.password)
            print(str(valor))

            # Imprime los permisos
            # for permission in user_permissions:
            #  print(permission)
            #usuario = request.user
            #user = request.user

            return redirect('menu')  # Cambia 'home' por el nombre de tu vista principal
        else:
            errors = "Invalid login credentials."
            titulo = "INICIAR SESION"

            return render(request, 'base/login.html', {'messages': errors, 'title': titulo})

    else:
        errors = ""
        if request.user.is_authenticated:
            logout(request)

        titulo= "INICIAR SESION"
    return render(request, 'base/login.html', {'messages': errors, 'title':titulo})


def sisa(request):
 return render (request, "base/sisa.html")

#def login(request):
#    return render(request, "base/login.html")

def menuini(request):
    return render(request, "base/menu-ini.html")
def pagcofirmacion(request):
    return render(request, "base/pagcofirmacion.html")
def logoini(request):
    return render(request, "base/logo-ini.html")

def buscar_usuario(request):
    if request.method == "POST":
        usu = request.POST['user']
        psw = request.POST['psw']
        n="{"+ usu +","+ psw +"}"
        sql = "select controlusuario('" + n + "');"
        valor1 = retorno_valor(con1, sql, usu, psw)
        print(valor1)
        if valor1 is False:
            valor2= False;
        else:
             valor2 = valor1[0]
        data = {
            'user': valor2,
         }
        Response = JsonResponse({'datos': data})
    return Response

def menu(request):
    if request.user.is_authenticated:

        contexto = {
            'habcmp': True,
            'habprov': True

        }


        return render(request, "base/menu.html",contexto)
    else:
        return redirect('login')

def base(request):
    n1 = request.POST['user']
    data = {
        'usuario': n1,
    }
    return render(request, "base/base.html",{'datos': data})

def casap(request):
    return render(request, "base/casap.html")

def login2(request):
    return render(request, "base/login2.html")

