from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils.datetime_safe import datetime

from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import desencriptar_dato, encriptar_dato, desencriptar_datos, encriptar_datos
from ventas.models import Ventascuotas, Ventacab


def ventascuotas_cargar(request,pk_token):
    if not request.user.has_perm('ventas.view_ventascuotas'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response


    if pk_token == "0":
        return redirect('ventascab_cargar', pk_token=0)
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    pk_tokens = int(desencriptar_datos(pk_token,skey))
    objetos = Ventacab.objects.filter(idventacab=pk_tokens)
    for objeto in objetos:
        fecha= objeto.fecha
        nrofactura= objeto.nrofactura
        cliente= objeto.cliente
        total= f"{(objeto.total):,.0f}"

       # moneda= objeto.moneda,
       # cotizacion= objeto.cotizacion,


    contexto = {
        'habcmp': True,
        'habprov': True,
        'pkf': pk_token,
        'fecha': fecha,
        'nrofactura': nrofactura,
        'cliente': cliente,
        'total': total,
        'title': 'CUOTAS CLIENTES'
    }

    return render(request, "ventas/ventascuotas.html", contexto)

def ventascuotas_generar(request):
    if not request.user.has_perm('ventas.add_ventascuotas'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response
    pkf = request.POST['pkf']
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    idventacab = int(desencriptar_datos(pkf,skey))
    entrega =float(request.POST['entrega'])
    fechavto = request.POST['fechavto']
    cuota = float(request.POST['cuota'])
    monto = float(float(request.POST['monto']))
    entregainicial=0
    icuota=0
    imonto=0

    obj = Ventacab.objects.filter(idventacab=idventacab)
    idcliente = ([(detalle.idcliente) for detalle in obj])[0]
    # print(" idcliente "+ str(idcliente))

    if isinstance(entrega, int) or isinstance(entrega, float):
        entregainicial=entrega
    if isinstance(cuota, int) or isinstance(cuota, float):
        icuota = cuota
    if isinstance(monto, int) or isinstance(monto, float):
        imonto = monto
    print(" entregainicial "+str(entregainicial))
    print(" icuota "+str(icuota))
    print(" imonto "+str(imonto))
    print(" fechavto "+str(fechavto))
    print(" idcliente "+str(idcliente))

    ventascuotas = Ventascuotas.objects.filter(idventacab=idventacab)
    ventascuotas.delete()

    fechavto = datetime.strptime(fechavto, '%Y-%m-%d')
    contador = 0

    while contador <= icuota:
        imontocuota=entregainicial
        if contador>0:
            fechavto = fechavto + timedelta(days=30)  # Sumamos 30 días (un mes aproximado)
            imontocuota=imonto

        if imontocuota>0:
            ventascuotas = Ventascuotas()
            ventascuotas.idventacab = float(idventacab)
            ventascuotas.orden = contador
            ventascuotas.idcliente=idcliente
            ventascuotas.fechavto = fechavto
            ventascuotas.monto = imontocuota
            ventascuotas.saldo = imontocuota

            ventascuotas.save()
        contador=contador+1

    response = {'success': True}
    return JsonResponse(response)


def ventascuotas_listar(request):
    if not request.user.has_perm('ventas.view_ventascuotas'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pk = request.POST['id_pk']
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)

    idventacab = int(desencriptar_datos(pk,skey))
    orden = request.POST['orden']
    formato = "%d-%m-%Y"  # Por ejemplo, "09-10-2023 15:30:00"
    print("idventacab  " + str(idventacab))

    if int(orden) == -1:
        objetos = Ventascuotas.objects.filter(idventacab=idventacab).order_by('orden')
        formato = "%d-%m-%Y"  # Por ejemplo, "09-10-2023 15:30:00"

    if int(orden) >=0:
        objetos = Ventascuotas.objects.filter(idventacab=idventacab,orden=orden)
        formato = "%y-%m-%d"  # Por ejemplo, "09-10-2023 15:30:00"

    datos = []
   # 'fechavto': objeto.fechavto.strftime(formato),

    for objeto in objetos:
        datos.append({
            'pkfd': encriptar_datos(objeto.idventascuotas,skey),
            'orden': objeto.orden,
            'fechavto': objeto.fechavto.strftime(formato),
            'monto': f"{(objeto.monto):,.0f}",
            'monto2':objeto.monto,
        })

    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})
    return Response


def ventascuotas_eliminar(request, pk_token):
    if not request.user.has_perm('ventas.delete_ventascuotas'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    pk = int(desencriptar_datos(pk_token,skey))

    objetos = Ventascuotas.objects.filter(idventascuotas=pk)
    for objeto in objetos:
        idventacab= objeto.idventacab

    ventascuotas = get_object_or_404(Ventascuotas, pk=pk)
    ventascuotas.delete()

    orden=0
    objetos = Ventascuotas.objects.filter(idventacab=idventacab,orden__gt=0).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden=orden+1
        objeto.save()

    response = {'success': True, 'message': ''}
    return JsonResponse(response)


def ventascuotas_mod(request):
    if not request.user.has_perm('ventas.change_ventascuotas'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pkf = request.POST['pkf']
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        idventacab = int(desencriptar_datos(pkf,skey))
        orden = request.POST['orden']
        monto = request.POST['monto']
        fechavto = request.POST['fechavto']

        objetos = Ventascuotas.objects.filter(idventacab=idventacab,orden=orden)
        for ventascuotas in objetos:
            idventascuotas=ventascuotas.idventascuotas

        ventascuotas = get_object_or_404(Ventascuotas, pk=idventascuotas)
        ventascuotas.idventacab =float(idventacab)
        ventascuotas.orden = orden
        ventascuotas.fechavto = fechavto
        ventascuotas.monto = monto
        ventascuotas.saldo = monto
        ventascuotas.save()

        response = {'success': True}
        return JsonResponse(response)

def ventascuotas_guardar(request):
    if not request.user.has_perm('ventas.add_ventascuotas'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pkf = request.POST['pkf']
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        idventacab = int(desencriptar_datos(pkf,skey))
        print("idventacab" +str(idventacab))
        monto = request.POST['monto']

        fechavto = request.POST['fechavto']

        obj = Ventacab.objects.filter(idventacab=idventacab)
        idcliente = ([(detalle.idcliente) for detalle in obj])[0]
        # print(" idcliente "+ str(idcliente)

        cantr = Ventascuotas.objects.filter(idventacab=idventacab ,orden__gt=0).count()+1
        print("cantr" +str(cantr))

        ventascuotas = Ventascuotas()
        ventascuotas.idventacab =float(idventacab)
        ventascuotas.orden = cantr
        ventascuotas.fechavto = fechavto
        ventascuotas.monto = monto
        ventascuotas.idcliente = idcliente
        ventascuotas.saldo = monto
        ventascuotas.save()

        response = {'success': True}
        return JsonResponse(response)
