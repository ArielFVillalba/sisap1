from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from compras.forms import *

from django.contrib import messages
from django.core.serializers import json

from ventas.forms import VentacabForm, OrdenVentacabForm
from ventas.models import *


def ventacab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'ventas/ventacab_filt.html')

def ventacab_filtro_lst(request):
    if not request.user.is_authenticated:
        return redirect('login')
    idcliente = request.GET.get('idcliente', '')
    fechaini = request.GET.get('fechaini', '')
    fechafin = request.GET.get('fechafin', '')
    tipodoc = request.GET.get('tipodoc', '')
    ventacab = Ventacab.objects.all()
    if idcliente == '':
        idcliente = 0
    if ventacab.exists() and int(idcliente) >= 1:
        ventacab = ventacab.filter(idcliente__contains=idcliente)
    if ventacab.exists() and fechaini:
        fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
        ventacab = ventacab.filter(fecha__gte=fecha_inicio)
    if ventacab.exists() and fechafin:
        fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
        ventacab = ventacab.filter(fecha__lte=fecha_fin)
    if ventacab.exists() and tipodoc:
        ventacab = ventacab.filter(tipodoc=tipodoc)
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)

    for objeto in ventacab:
        objeto.pkf = encriptar_datos(objeto.idventacab,skey)
        objeto.save()

    cadena = ""
    return render(request, 'ventas/ventacab_listar.html', {'ventacab': ventacab, 'cadena': cadena})


def ventacab_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')

    if cadena == "*":
        ventacab = Ventacab.objects.all()
        return render(request, 'ventas/ventacab_listar.html', {'ventacab': ventacab, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'ventas/ventacab_listar.html')

    qs = Ventacab.objects.filter(nombre=0)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Cliente.objects.filter(fecha__contains=subcadenas[i])
        qs = qs.union(qs1)
        qs2 = Cliente.objects.filter(nrofactura__contains=subcadenas[i])
        qs = qs.union(qs2)
        qs3 = Cliente.objects.filter(cliente__contains=subcadenas[i])
        qs = qs.union(qs3)
        qs4 = Cliente.objects.filter(ruc__contains=subcadenas[i])
        qs = qs.union|(qs4)

    ventacab = qs
    return render(request, 'ventas/ventacab_listar.html', {'ventacab': ventacab, 'cadena': cadena})


class ventacab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.view_ventacab'
    model = Ordenventacab
    form_class = OrdenVentacabForm
    template_name = 'ventas/ventacab.html'
    success_url = reverse_lazy('ventacab_cargar')

    def get(self, request,pk_token):
        ventacab = None
        if pk_token != "0":
            skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
            pk_desencriptado = desencriptar_datos(pk_token,skey)
            ventacab = Ventacab.objects.get(idventacab=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'ventacab': ventacab}  # Crear un diccionario de contexto
        context['title'] = '   VENTA  '
        context['sidr'] = '/Ventacab/' + str(pk_token) + '/cargar/'
        context['pkf'] = pk_token
        context['pk_token'] = pk_token
        context['hab1']= True
        context['hab2']= False

        return render(request, self.template_name, context)

class ventacab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'ventas.add_ordenventacab'

    model = Ventacab
    form_class = VentacabForm
    template_name = 'ventas/ventacab.html'
    success_url = reverse_lazy('ventacab_crear')
    def dispatch(self, *args, **kwargs):
        return super(ventacab_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CARGAR VENTA '
        context['sidr'] = '/ventacab/crear/'
        context['hab1']= False
        context['hab2']= True
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'ventas creado exitosamente.')
        skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
        pk_encriptado = encriptar_datos(self.object.pk,skey)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('ventacab_cargar', pk_token=str(pk_encriptado))

class ventacab_editar(UpdateView):
    permission_required = 'ventas.change_ordenventacab'
    model = Ventacab
    form_class = VentacabForm
    template_name = 'ventas/ventacab.html'
    success_url = '/ventacab/0/listar/'

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
            pk = desencriptar_datos(pk_token,skey)
            return get_object_or_404(Ventacab, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' EDITAR  VENTA  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/ventacab/'+str(pk_token)+'/editar/'
        context['pk_token'] = pk_token
        context['pkf'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return redirect('ventacab_cargar', pk_token=str(pk_token))

class ventacab_eliminar(LoginRequiredMixin, ValidarPermisoMixin, View):
    permission_required = 'ventas.delete_ventacab'

    def get(self, request, pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO  "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')

        if action == 'CONFIRMAR':
            skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
            pk = desencriptar_datos(pk_token,skey)
            instance = get_object_or_404(Ventacab, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, 'orden eliminado exitosamente.')
            return redirect('ventacab_cargar', pk_token=0)
        else:
            return redirect('ventacab_cargar', pk_token=str(pk_token))

def ventadet_listar(request):
    if not request.user.has_perm('ventas.view_ventadet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    idventacab = request.POST['pkf']
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)

    idventacab = desencriptar_datos(idventacab,skey)


    orden = request.POST['orden']
    if int(orden) == 0:
        objetos = Ventadet.objects.filter(idventacab=idventacab).order_by('orden')
    if int(orden) >=1:
        objetos = Ventadet.objects.filter(idventacab=idventacab,orden=orden)
    datos = []

    for objeto in objetos:
        datos.append({
            'pkfd': encriptar_datos(objeto.idventadet,skey),
            'orden': objeto.orden,
            'codigo': objeto.codigo,
            'descripcion': objeto.descripcion,
            'cantidad': f"{(objeto.cantidad):.3f}",
            'precio': f"{(objeto.precio):.0f}",
            'iva': f"{(objeto.iva):.0f}",
            'subtotal': f"{(objeto.precio * objeto.cantidad):.0f}"
        })

    # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})
    return Response



def actventacab(idventacab):

    #gravada10 = Ventadet.objects.filter(iva=10,idventacab=idventacab).aggregate(total=Sum('cantidad' * 'precio'))['total']

    detalles = Ventadet.objects.filter(iva=5,idventacab=idventacab)
    gravada5 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Ventadet.objects.filter(iva=10, idventacab=idventacab)
    gravada10 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Ventadet.objects.filter(iva=0, idventacab=idventacab)
    exenta = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    gravada=gravada10+gravada5
    total=gravada+exenta

    objetos = Ventacab.objects.filter(idventacab=idventacab)
    for objeto in objetos:
        objeto.gravada5 = gravada5
        objeto.gravada10 = gravada10
        objeto.gravada = gravada
        objeto.exenta = exenta
        objeto.total = total
        objeto.save()
        return total


def ventadet_guardar(request):
    if not request.user.has_perm('ventas.add_ventadet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        idventacab = request.POST['pkf']
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        idventacab = desencriptar_datos(idventacab,skey)

        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        deposito = request.POST['deposito']

        cantr = Ventadet.objects.filter(idventacab=idventacab).count()

        cantr=cantr+1
        articulos = Articulo.objects.filter(codigo=float(codigo))
        for articulo in articulos:
            ventadet = Ventadet()
            ventadet.idventacab =float(idventacab)
            ventadet.orden = cantr
            ventadet.idarticulo = articulo.idarticulo
            ventadet.codigo =  articulo.codigo
            ventadet.descripcion = articulo.descripcion
            ventadet.cantidad = float(cantidad)
            ventadet.unidad = articulo.unidad
            ventadet.costo =articulo.costo
            ventadet.precio = float(precio)
            ventadet.iva = articulo.iva
            ventadet.deposito = deposito

            ventadet.save()
            actventacab(idventacab)
            response = {'success': True}
            return JsonResponse(response)

def ventadet_editar(request):
    if not request.user.has_perm('ventas.add_ventadet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        idventacab = request.POST['pkf']
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        idventacab = desencriptar_datos(idventacab,skey)
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        orden = request.POST['orden']
        deposito = request.POST['deposito']



        objetos = Ventadet.objects.filter(idventacab=idventacab,orden=orden)
        for ventadet in objetos:
            idventadet=ventadet.idventadet

        articulos = Articulo.objects.filter(codigo=float(codigo))

        for articulo in articulos:
            ventadet = get_object_or_404(Ventadet, pk=idventadet)
            ventadet.idventacab =float(idventacab)
            ventadet.orden = orden
            ventadet.idarticulo = articulo.idarticulo
            ventadet.codigo =  articulo.codigo
            ventadet.descripcion = articulo.descripcion
            ventadet.cantidad = float(cantidad)
            ventadet.unidad = articulo.unidad
            ventadet.costo =articulo.costo
            ventadet.precio = float(precio)
            ventadet.iva = articulo.iva
            ventadet.deposito = deposito
            ventadet.save()
            actventacab(idventacab)
            response = {'success': True}
            return JsonResponse(response)

def ventadet_eliminar(request, pk_token):
    if not request.user.has_perm('ventas.delete_ventadet'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    idventadet = int(desencriptar_datos(pk_token,skey))

    objetos = Ventadet.objects.filter(idventadet=idventadet)
    for objeto in objetos:
        idventacab= objeto.idventacab

    ventadet = get_object_or_404(Ventadet, idventadet=idventadet)
    ventadet.delete()

    orden=0
    objetos = Ventadet.objects.filter(idventadet=idventadet).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden=orden+1
        objeto.save()

    actventacab(idventacab)

    response = {'success': True, 'message': ''}
    return JsonResponse(response)
