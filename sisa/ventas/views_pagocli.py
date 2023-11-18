from django.urls import reverse_lazy, reverse
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from .forms import *

from django.contrib import messages

from django.http import JsonResponse, FileResponse, HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
from inicio.funcion import *
from django.shortcuts import redirect
import datetime
from datetime import datetime
from django.shortcuts import get_object_or_404
from sisa.mixins import ValidarPermisoMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def pagoclicab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.has_perm('ventas.view_ventadet'):
        return redirect('login')

    return render(request, 'ventas/pagocli_filt.html')


def pagoclicab_filtro_lst(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.has_perm('ventas.view_pagoclientes'):
        return redirect('login')


    idcli = request.GET.get('idcli', '')
    fechaini = request.GET.get('fechaini', '')
    fechafin = request.GET.get('fechafin', '')
    pagoclientes = Pagoclientes.objects.all()
    if idcli == '':
        idcli = 0
    if pagoclientes.exists() and int(idcli) >= 1:
        pagoclientes = pagoclientes.filter(idcli__contains=idcli)
    if pagoclientes.exists() and fechaini:
        fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
        pagoclientes = pagoclientes.filter(fecha__gte=fecha_inicio)
    if pagoclientes.exists() and fechafin:
        fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
        pagoclientes = pagoclientes.filter(fecha__lte=fecha_fin)
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)

    for objeto in pagoclientes:
        objeto.pkf = encriptar_datos(objeto.idpagocliente,skey)

    cadena = ""
    return render(request, 'ventas/pagocli_listar.html', {'pagocliente': pagoclientes, 'cadena': cadena})


def pagoclicab_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.has_perm('ventas.view_pagoclientes'):
        return redirect('login')

    if cadena == "*":
        pagoclientes = Pagoclientes.objects.all()
        #compracab.objects.update(idcompracab=encriptar_dato(compracab.idcompracab))
        return render(request, 'ventas/pagocli_listar.html', {'pagoclientes': pagoclientes, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'ventas/pagocli_listar.html')

    qs = Pagoclientes.objects.filter(nombre=0)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Pagoclientes.objects.filter(fecha__contains=subcadenas[i])
        qs = qs.union(qs1)
        qs2 = Pagoclientes.objects.filter(nrofactura__contains=subcadenas[i])
        qs = qs.union(qs2)
        qs3 = Pagoclientes.objects.filter(cli__contains=subcadenas[i])
        qs = qs.union(qs3)
        qs4 = Pagoclientes.objects.filter(ruc__contains=subcadenas[i])
        qs = qs.union|(qs4)

    pagoclientes = qs

    return render(request, 'ventas/pagoclientes_listar.html', {'pagoclientes': pagoclientes, 'cadena': cadena})


class pagoclicab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.view_pagoclientes'
    model = Pagoclientes
    form_class = PagoclientesForm
    template_name = 'ventas/pagocliente.html'
    context_object_name = 'pagocliente'  # Nombre para acceder al objeto en la plantilla
    def get(self, request,pk_token):
        pagocliente = None
        if pk_token != "0":
            skey=str(self.request.user.last_login)+str(self.request.user.username)+str(self.request.user.password)
            pk_desencriptado = desencriptar_datos(pk_token,skey)
            pagocliente = Pagoclientes.objects.get(idpagocliente=pk_desencriptado)  # Recuperar la compra por su clave primaria
            #print (" pagocliente.fecha "+ str(pagocliente.fecha))
            #print (" pagocliente.recibo "+ str(pagocliente.recibo))
            #print (" pagocliente.cliente "+ str(pagocliente.cliente))


        context = {'pagocliente': pagocliente}  # Crear un diccionario de contexto
        context['title'] = '  PRAGO A CLIENTE  '
        context['sidr'] = '/pagoclicab/' + str(pk_token) + '/cargar/'
        context['pkf'] = pk_token
        context['hab1']= True
        context['hab2']= False

        return render(request, self.template_name, context)


class pagoclicab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'ventas.add_pagoclientes'
    model = Pagoclientes
    form_class = PagoclientesForm
    template_name = 'ventas/pagocliente.html'
    context_object_name = 'pagocliente'  # Nombre para acceder al objeto en la plantilla
    def dispatch(self, *args, **kwargs):
        return super(pagoclicab_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CARGAR PAGO CLIENTE '
        context['sidr'] = '/pagoclicab/crear/'
        context['hab1']= False
        context['hab2']= True
        return context

    def form_valid(self, form):
        messages.success(self.request, ' PAGO creado exitosamente.')
        response = super().form_valid(form)
        skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
        pk_encriptado = encriptar_datos(self.object.pk,skey)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('pagoclicab_cargar', pk_token=pk_encriptado)


class pagoclicab_editar(UpdateView):
    model = Pagoclientes
    form_class = PagoclientesForm
    template_name = 'ventas/pagocliente.html'
    context_object_name = 'pagocliente'  # Nombre para acceder al objeto en la plantilla
    success_url = '/pagoclicab/0/listar/'  # Nombre para acceder al objeto en la plantilla

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
            pk = desencriptar_datos(pk_token,skey)
            return get_object_or_404(Pagoclientes, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' EDITAR  VENTA  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/pagoclicab/'+str(pk_token)+'/editar/'
        context['pk_token'] = pk_token
        context['pkf'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return redirect('pagoclicab_cargar', pk_token=str(pk_token))


class pagopclicab_eliminar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.delete_pagoclientes'

    def get(self, request, pk_token):
        titulo = "¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg = " EL REGISTRO  "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg, 'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
        pk = desencriptar_datos(pk_token,skey)
        print("  pk " + str(pk))
        if action == 'CONFIRMAR':
            instance = get_object_or_404(Pagoclientes, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, ' eliminado exitosamente.')

            return redirect('pagoclicab_cargar', pk_token=0)
        else:
            return redirect('pagoclicab_cargar', pk_token=pk_token)


def pagoclifact_listar(request):
    if not request.user.has_perm('ventas.view_pagoclientesfact'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    pk = request.POST['id_pk']
    idpagoclientes = int(desencriptar_datos(pk,skey))
    orden = request.POST['orden']

    if int(orden) == 0:
        objetos = Pagoclifact.objects.filter(idpagocliente=idpagoclientes).order_by('orden')
    if int(orden) >= 1:
        objetos = Pagoclifact.objects.filter(idpagocliente=idpagoclientes, orden=orden)

   # print(str(objetos.count()))

    datos = []

    for objeto in objetos:
        factura = ''
        idventascuotas = int(objeto.idventascuotas)
        obj = Ventascuotas.objects.filter(idventascuotas=idventascuotas)
        idventacab = ([int(detalle.idventacab) for detalle in obj])[0]
        obj = Ventascuotas.objects.filter(idventascuotas=idventascuotas)
        #print(" idventascuotas "+ str(idventascuotas))

        nrocuota = ([(detalle.orden) for detalle in obj])[0]
        #print(" nrocuota "+ str(nrocuota))
        obj = Ventacab.objects.filter(idventacab=idventacab)
        factura = ([(detalle.nrofactura) for detalle in obj])[0]

        formato = "%y-%m-%d"  # Por ejemplo, "09-10-2023 15:30:00"
        fecha = objeto.fecha.strftime(formato)
        fecha = datetime.strptime(fecha, "%y-%m-%d")
        fecha = str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year)

        datos.append({
            'pkfd': encriptar_datos(objeto.idpagoclifact,skey),
            'orden': objeto.orden,
            'fecha':fecha,
            'factura': factura,
            'nrocuota': nrocuota,
            'saldo': f"{(objeto.saldo):.0f}",
            'monto': f"{(objeto.monto):.0f}",
        })
      #  print(" datos   " + str(datos))

    Response = JsonResponse({'datos':datos,'success': True, 'message': ''})
    return Response

class pagoclifact_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'ventas.delete_Pagoclientesfact'

    def get(self, request, pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO  "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        pk = desencriptar_datos(pk_token,skey)
        obj = Pagoclifact.objects.filter(idpagoclifact=pk)

        pk_token2 = (int(([(detalle.idpagocliente) for detalle in obj])[0]))
        pk_token3 = encriptar_datos(pk_token2,skey)
        print ("  pk_token2 " +str(pk_token2))
        print ("  pk_token3 " +str(pk_token3))

        if action == 'CONFIRMAR':
            instance = get_object_or_404(Pagoclifact, pk=pk)
            try:
                instance.delete()
                orden = 0
                objetos = Pagoclifact.objects.filter(idpagocliente=pk_token2).order_by('orden')
                for objeto in objetos:
                    objeto.orden = orden = orden + 1
                    objeto.save()

            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, ' eliminado exitosamente.')

            return redirect('pagoclicab_cargar', pk_token=pk_token3)
        else:
            return redirect('pagoclicab_cargar', pk_token=pk_token3)



class pagocliafact_listar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.view_Pagoclientesfact'

    def get(self, request, pk_token):
        if pk_token == "0":
            return redirect('pagoclicab_cargar', pk_token=0)
        datos = []
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        idpagoclientes = desencriptar_datos(pk_token,skey)
        #print(" pagocliafact_listar "+ str(idpagoclientes))


        obj = Pagoclientes.objects.filter(idpagocliente=idpagoclientes)
        idcliente = ([(detalle.idcliente) for detalle in obj])[0]
        #print(" idcliente "+ str(idcliente))

        objetos = Ventascuotas.objects.filter(idcliente=idcliente,saldo__gt=0).order_by('fechavto')  # Recuperar la compra por su clave primaria
        cantr = Ventascuotas.objects.filter(idcliente=idcliente).count()
        #print(" cantr "+ str(cantr))

        for objeto in objetos:
            formato = "%y-%m-%d"  # Por ejemplo, "09-10-2023 15:30:00"

            idventacab = int(objeto.idventacab)
            obj = Ventacab.objects.filter(idventacab=idventacab)
            factura = ([(detalle.nrofactura) for detalle in obj])[0]
            fecha = ([(detalle.fecha) for detalle in obj])[0].strftime(formato)
            fecha = datetime.strptime(fecha, "%y-%m-%d")
            fecha =  str(fecha.day) + "-"+ str(fecha.month) + "-"+str(fecha.year)
            total = ([(detalle.total) for detalle in obj])[0]
            formato = "%y-%m-%d"  # Por ejemplo, "09-10-2023 15:30:00"
            fechavto=objeto.fechavto.strftime(formato)
            fechavto = datetime.strptime(fechavto, "%y-%m-%d")
            fechavto =  str(fechavto.day) + "-"+ str(fechavto.month) + "-"+str(fechavto.year)

            datos.append({
                'pkfd': encriptar_datos(objeto.idventascuotas,skey),
                'pkpp': encriptar_datos(idpagoclientes,skey),
                'fechafactura': fecha,
                'factura': factura,
                'total': f"{(total):,.0f}",
                'fechavto': fechavto,
                'cuota': objeto.orden,
                'saldo': f"{(objeto.saldo):,.0f}",
                'monto': f"{(objeto.monto):,.0f}",
            })

        return render(request, 'ventas/clicuotalst.html', {'cuota': datos,'pk_token': pk_token})


class pagoclifact_agregar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.add_Pagoclientesfact'

    def get(self, request, pk_token1,pk_token2):
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)

        idpagoclientes = desencriptar_datos(pk_token1,skey)
        idventascuotas = desencriptar_datos(pk_token2,skey)
        print(" idpagoclientes "+ str(idpagoclientes))
        print(" idventascuotas "+ str(idventascuotas))

        objetos = Ventascuotas.objects.filter(idventascuotas=idventascuotas)
        for objeto in objetos:
            pagoclientesfact = Pagoclifact()
            pagoclientesfact.idpagocliente = float(idpagoclientes)
            pagoclientesfact.idventascuotas = idventascuotas
            pagoclientesfact.orden = objeto.orden
            pagoclientesfact.fecha = objeto.fechavto
            pagoclientesfact.saldo = objeto.saldo
            pagoclientesfact.monto = objeto.saldo
            pagoclientesfact.save()

            orden = 0
            objetos = Pagoclifact.objects.filter(idpagocliente=idpagoclientes).order_by('idpagoclifact')
            for objeto in objetos:
                objeto.orden = orden = orden + 1
                objeto.save()

        return redirect('pagoclicab_cargar', pk_token=pk_token1)


def pagoclifact_editar(request):
    if not request.user.has_perm('ventas.change_pagoclientesfact'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)

        pkf = request.POST['pkf']
        idpagoclientes = int(desencriptar_datos(pkf,skey))
        orden = request.POST['orden']
        monto = request.POST['monto']


        objetos = Pagoclifact.objects.filter(idpagocliente=idpagoclientes, orden=orden)
        idventascuotas= ([(detalle.idventascuotas) for detalle in objetos])[0]
        anterior = sum([ detalle.monto for detalle in objetos])
        objetos = Pagoclifact.objects.filter(idventascuotas=idventascuotas)
        totalpagado = sum([ detalle.monto for detalle in objetos])
        obj = Ventascuotas.objects.filter(idventascuotas=idventascuotas)
        cuota = (int(([(detalle.monto) for detalle in obj])[0]))
        saldo=float(totalpagado)-float(anterior)+float(monto)
        saldo=float(cuota)-saldo
        valmax=float(cuota)-(float(totalpagado)-float(anterior))

        #print (" anterior " + str(anterior))
        #print (" totalpagado " + str(totalpagado))
        #print (" cuota " + str(cuota))
        #print (" monto " + str(monto))
        #print (" saldo " + str(saldo))
        #print (" valmax " + str(valmax))

        if saldo < 0:
            response = {'success': False, 'message': 'Monto supera la cuota valor maximo '+ str(valmax)}
            return JsonResponse(response)

        objetos = Pagoclifact.objects.filter(idpagocliente=idpagoclientes,orden=orden)
        for objeto in objetos:
            objeto.monto = monto
            objeto.save()
        response = {'success': True}
        return JsonResponse(response)


def pagoclipago_listar(request):
    if not request.user.has_perm('ventas.view_Pagoclientesforma'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pk_token = request.POST['id_pk']
    if pk_token == "0":
        return redirect('pagoclientescab_cargar', pk_token=0)

    pk = request.POST['id_pk']
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    idpagoclientes = int(desencriptar_datos(pk,skey))
    print(" pagoclipago - idpagoclientes " + str(idpagoclientes))
    orden = request.POST['orden']

    if int(orden) == 0:
        objetos = Pagocliforma.objects.filter(idpagocliente=idpagoclientes)
    if int(orden) >= 1:
        objetos = Pagocliforma.objects.filter(idpagocliente=idpagoclientes)

    datos = []
    tipopago = ['efectivo', 'cheque', 'tarjeta']

    print(str(objetos.count()))
    if objetos.count()>0:
        for objeto in objetos:
            itipopago = objeto.idtipopago
            stp = tipopago[int(itipopago)]

            datos.append({
                'pkpf': encriptar_datos(objeto.idpagocliforma, skey),
                'tipopago': stp,
                'monto': f"{(objeto.monto):,.0f}",
                'nrodoc': objeto.nrodoc,
                'banco': objeto.banco,
                'ctacte': objeto.ctacte,
            })
        #  print(" datos   " + str(datos))

    Response = JsonResponse({'datos': datos, 'success': True, 'message': ''})
    return Response


def pagoclipago_agregar(request):
    if not request.user.has_perm('ventas.add_pagoclientesforma'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)

        pkf = request.POST['pkf']
        idpagoclientes = int(desencriptar_datos(pkf,skey))
        idtipopago = request.POST['tipopago']
        montop = request.POST['montop']
        nrodoc = request.POST['nrodoc']
        banco = request.POST['banco']
        ctacte= request.POST['ctacte']

        tipopago = ['efectivo', 'cheque', 'tarjeta']
        obj = Pagoclientes.objects.filter(idpagocliente=idpagoclientes)
        idcli = ([(detalle.idcliente) for detalle in obj])[0]
        fecha = ([(detalle.fecha) for detalle in obj])[0]

        for i in range(3):
            if idtipopago==tipopago[i]:
                idtipopago=i

        pvf = Pagocliforma()
        pvf.idpagocliente=idpagoclientes
        pvf.idtipopago = idtipopago
        pvf.monto = montop
        pvf.nrodoc = nrodoc
        pvf.fecha=fecha
        pvf.banco=banco
        pvf.idcliente = idcli
        pvf.ctacte = ctacte
        pvf.save()
        response = {'success': True}
        return JsonResponse(response)


class pagoclipago_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'ventas.delete_pagoclientesforma'

    def get(self, request,pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO  "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        pk = desencriptar_datos(pk_token,skey)
        #print ("  pk " +str(pk))

        obj = Pagocliforma.objects.filter(idpagocliforma=pk)
        pk_token2 = (int(([(detalle.idpagocliente) for detalle in obj])[0]))
        pk_token3 = encriptar_datos(pk_token2,skey)
       # print ("  pk_token " +str(pk))
        #print ("  pk_token2 " +str(pk_token2))
        #print ("  pk_token3 " +str(pk_token3))

        if action == 'CONFIRMAR':
            instance = get_object_or_404(Pagocliforma, pk=pk)
            try:
                instance.delete()

            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, ' eliminado exitosamente.')

            return redirect('pagoclicab_cargar', pk_token=pk_token3)
        else:
            return redirect('pagoclicab_cargar', pk_token=pk_token3)



