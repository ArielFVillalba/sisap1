from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from inicio.funcion import *
from django.contrib import messages
from django.core.serializers import json
from django.db.models import Sum

from stock.models import Deposito

con1=1


def menustock(request):
    if request.user.is_authenticated:
        return render(request, "stock/menustock.html")
    else:
        return redirect('login')

    #request.COOKIES.get
    #usu = request.COOKIES.get('usuario')
    #psw = request.COOKIES.get('contraseña')
    #tipo = "dep"
    #modulo = "compras"
    #n = "{" + usu + "," + psw+ "," +  tipo + "," +  modulo +"}"
    #sql = "select controlingresomod('" + n + "');"
    #valor1 = seleccionar_datos2(con1, sql, usu, psw)
    #if valor1 == 'true':
    #else:
    #    return render(request, template_name="base/menu.html/")

def deposito(request):
    request.COOKIES.get
    #usu = request.COOKIES.get('usuario')
    #psw = request.COOKIES.get('contraseña')
    #tipo = "dep"
    #modulo = "compras"
    #n = "{" + usu + "," + psw+ "," +  tipo + "," +  modulo +"}"
    #sql = "select controlingresomod('" + n + "');"
    #valor1 = seleccionar_datos2(con1, sql, usu, psw)
    #if valor1 == 'true':
    return render(request, "stock/deposito.html")
    #else:
    #    return render(request, template_name="base/menu.html/")



def deposito_agregar(request):
    if request.method == 'POST':
        deposita = request.POST['deposito']
        sucursal = request.POST['sucursal']
        deposito = Deposito()
        deposito.deposito = deposita
        deposito.sucursal = sucursal
        deposito.save()

        response = {'success': True}
        return JsonResponse(response)

def deposito_editar(request):
    if request.method == 'POST':
        deposita = request.POST['deposito']
        sucursal = request.POST['sucursal']

        var=True

        if deposita is None or deposita == "":
            var=False
        if sucursal is None or sucursal == "":
            var=False

        if var == False:
            response = {'success': False}
            return JsonResponse(response)

        habilitado = True
        depositaf=""
        objetos = Deposito.objects.filter(deposito=deposita)
        for objeto in objetos:
            depositaf = objeto.deposito
        if depositaf:
            deposito = get_object_or_404(Deposito, deposito=deposita)

        if not depositaf:
            deposito = Deposito()



        deposito.deposito = deposita
        deposito.sucursal = sucursal
        deposito.habilitado= habilitado
        deposito.save()

        response = {'success': True}
        return JsonResponse(response)


def deposito_eliminar(request,pk_token):
    print('entra en eli '+str(pk_token))
    deposit = get_object_or_404(Deposito, deposito=pk_token)
    deposit.delete()
    response = {'success': True}
    return JsonResponse(response)

def deposito_listar(reqduest):
    objetos = Deposito.objects.all()
    datos = []
    for objeto in objetos:
        datos.append({
            'deposito': objeto.deposito,
            'sucursal': objeto.sucursal,
        })

    # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
    Response = JsonResponse({'datos': datos})
    return Response


def cmbdep(request):
    if request.method == 'POST':
        deposito = Deposito.objects.all().values_list('deposito', flat=True)
        nombres = list(deposito)
        Response = JsonResponse({'datos': nombres})
        return Response
