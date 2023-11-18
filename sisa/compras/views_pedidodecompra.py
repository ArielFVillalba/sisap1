from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from .forms import *
from django.contrib import messages
from django.core.serializers import json
from django.db.models import Sum


def pedidocompcab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'compras/pedidodecompra_filt.html')

def pedidocompcab_filtro_lst(request):
    if not request.user.is_authenticated:
        return redirect('login')

    idproveedor =  request.GET.get('idproveedor', '')
    fechaini =  request.GET.get('fechaini', '')
    fechafin =  request.GET.get('fechafin', '')
    tipodoc =  request.GET.get('tipodoc', '')
    pedidocompcab = Pedidocompcab.objects.all()

    if idproveedor=='':
        idproveedor=0
    if pedidocompcab.exists() and int(idproveedor) >=1:
            pedidocompcab = pedidocompcab.filter(idproveedor__contains=idproveedor)
    if pedidocompcab.exists() and  fechaini:
            fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
            pedidocompcab = pedidocompcab.filter(fecha__gte=fecha_inicio)
    if pedidocompcab.exists() and  fechafin:
            fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
            pedidocompcab = pedidocompcab.filter(fecha__lte=fecha_fin)
    if pedidocompcab.exists() and tipodoc:
        pedidocompcab = pedidocompcab.filter(tipodoc=tipodoc)

    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    for objeto in pedidocompcab:
        objeto.pkpc = encriptar_datos(objeto.idpedidocompcab,skey)

    cadena=""
    return render(request, 'compras/pedidodecompra_lst.html', {'pedidocompcab': pedidocompcab, 'cadena': cadena })

def pedidocompcab_listar(request,cadena):
    if cadena == "*":
        print("valor"+ cadena)
        pedidocompcab = Pedidocompcab.objects.all()
        return render(request, 'compras/pedidodecompra_lst.html', {'pedidocompcab': pedidocompcab, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'compras/pedidodecompra_lst.html')

    qs = Pedidocompcab.objects.filter(nombre=0)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Pedidocompcab.objects.filter(fecha__contains=subcadenas[i])
        qs = qs.union(qs1)
        qs2 = Pedidocompcab.objects.filter(nrofactura__contains=subcadenas[i])
        qs = qs.union(qs2)
        qs3 = Pedidocompcab.objects.filter(proveedor__contains=subcadenas[i])
        qs = qs.union(qs3)
        qs4 = Pedidocompcab.objects.filter(ruc__contains=subcadenas[i])
        qs = qs.union|(qs4)

    pedidocompcab = qs
    return render(request, 'compras/pedidodecompra_lst.html', {'pedidocompcab': pedidocompcab, 'cadena': cadena})

class pedidocompcab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'compras.view_pedidocompcab'
    model = Pedidocompcab
    form_class = PedidodecompcabForm
    template_name = 'compras/pedidodecompra.html'
    success_url = reverse_lazy('pedidocompcab_crear')

    def get(self, request,pk_token):
        pedidocompcab = None
        if pk_token != "0":
            skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
            pk_desencriptado = desencriptar_datos(pk_token,skey)
            pedidocompcab = Pedidocompcab.objects.get(idpedidocompcab=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'pedidocompcab': pedidocompcab}  # Crear un diccionario de contexto
        context['title'] = '  PEDIDO COMPRA  '
        context['sidr'] = '/pedidocompcab/' + str(pk_token) + '/cargar/'
        context['pk_token'] = pk_token
        context['pkpc'] = pk_token
        context['hab1']= True
        context['hab2']= False
        return render(request, self.template_name, context)

class pedidocompcab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'compras.add_pedidocompcab'
    model = Pedidocompcab
    form_class = PedidodecompcabForm
    template_name = 'compras/pedidodecompra.html'
    success_url = reverse_lazy('pedidocompcab_crear')
    def dispatch(self, *args, **kwargs):
        return super(pedidocompcab_crear, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CARGAR PEDIDO DE COMPRA '
        context['sidr'] = '/pedidocompcab/crear/'
        context['hab1']= False
        context['hab2']= True
        return context

    def form_valid(self, form):
        messages.success(self.request, ' Pedido de compra creado exitosamente.')
        response = super().form_valid(form)
        skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
        pk_encriptado = encriptar_datos(self.object.pk,skey)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('pedidocompcab_cargar', pk_token=pk_encriptado)

class pedidocompcab_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'compras.change_pedidocompcab'
    model = Pedidocompcab
    form_class = PedidodecompcabForm
    template_name = 'compras/pedidodecompra.html'


    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
            pk = desencriptar_datos(pk_token,skey)
            return get_object_or_404(Pedidocompcab, pk=pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '  EDITAR PEDIDO  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/pedidocompcab/' + pk_token + '/editar/'
        context['pk_token'] = pk_token
        context['pkpc'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def get_success_url(self):
        messages.success(self.request, ' editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return reverse_lazy('pedidocompcab_cargar', kwargs={'pk_token': pk_token})


class pedidocompcab_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'compras.delete_pedidocompcab'

    def get(self, request, pk_token):
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        pk = desencriptar_datos(pk_token,skey)
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO  "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')

        if action == 'CONFIRMAR':
            skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
            pk = desencriptar_datos(pk_token,skey)
            instance = get_object_or_404(Pedidocompcab, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, ' eliminado exitosamente.')
            return redirect('pedidocompcab_cargar', pk_token=0)
        else:
            return redirect('pedidocompcab_cargar', pk_token=pk_token)


def pedidocompdet_listar(request):
    if not request.user.has_perm('compras.view_pedidocompdet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pkpc = request.POST['pkpc']
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    idpedidocompcab = desencriptar_datos(pkpc,skey)

    orden = request.POST['orden']
    if int(orden) == 0:
        objetos = Pedidocompdet.objects.filter(idpedidocompcab=idpedidocompcab).order_by('orden')
    if int(orden) >=1:
        objetos = Pedidocompdet.objects.filter(idpedidocompcab=idpedidocompcab,orden=orden)
    datos = []

    for objeto in objetos:
        datos.append({
            'pkpcd': encriptar_datos(objeto.idpedidocompdet,skey),
            'orden': objeto.orden,
            'codigo': objeto.codigo,
            'descripcion': objeto.descripcion,
            'cantidad': objeto.cantidad,
            'precio': f"{(objeto.precio):.0f}",
            'iva': f"{(objeto.iva):.0f}",
            'subtotal': f"{(objeto.precio * objeto.cantidad):.0f}"
        })


    # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})
    return Response


def actpedidocompracab(idpedidocompcab):

    #gravada10 = Compradet.objects.filter(iva=10,idcompracab=idcompracab).aggregate(total=Sum('cantidad' * 'precio'))['total']

    detalles = Pedidocompdet.objects.filter(iva=5,idpedidocompcab=idpedidocompcab)
    gravada5 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Pedidocompdet.objects.filter(iva=10, idpedidocompcab=idpedidocompcab)
    gravada10 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Pedidocompdet.objects.filter(iva=0, idpedidocompcab=idpedidocompcab)
    exenta = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    gravada=gravada10+gravada5
    total=gravada+exenta

    objetos = Pedidocompcab.objects.filter(idpedidocompcab=idpedidocompcab)
    for objeto in objetos:
        objeto.gravada5 = gravada5
        objeto.gravada10 = gravada10
        objeto.gravada = gravada
        objeto.exenta = exenta
        objeto.total = total
        objeto.save()
    return total


def pedidocompdet_guardar(request):
    if not request.user.has_perm('compras.add_pedidocompdet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)
    if request.method == 'POST':

        pkpc = request.POST['pkpc']
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        idpedidocompcab = desencriptar_datos(pkpc,skey)

        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        cantr = Pedidocompdet.objects.filter(idpedidocompcab=idpedidocompcab).count()
        print("entra en pediod det")
        cantr=cantr+1
        articulos = Articulo.objects.filter(codigo=float(codigo))
        for articulo in articulos:
            pedidocompdet = Pedidocompdet()
            pedidocompdet.idpedidocompcab =float(idpedidocompcab)
            pedidocompdet.orden = cantr
            pedidocompdet.idarticulo = articulo.idarticulo
            pedidocompdet.codigo =  articulo.codigo
            pedidocompdet.descripcion = articulo.descripcion
            pedidocompdet.cantidad = float(cantidad)
            pedidocompdet.unidad = articulo.unidad
            pedidocompdet.costo =articulo.costo
            pedidocompdet.precio = float(precio)
            pedidocompdet.iva = articulo.iva
            pedidocompdet.save()
            actpedidocompracab(idpedidocompcab)
            response = {'success': True}
            return JsonResponse(response)

def pedidocompdet_editar(request):
    if not request.user.has_perm('compras.change_pedidocompdet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pkpc = request.POST['pkpc']
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        idpedidocompcab = desencriptar_datos(pkpc,skey)
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        orden = request.POST['orden']
        objetos = Pedidocompdet.objects.filter(idpedidocompcab=idpedidocompcab,orden=orden)
        for pedidocompdet in objetos:
            idpedidocompdet=pedidocompdet.idpedidocompdet

        articulos = Articulo.objects.filter(codigo=float(codigo))
        for articulo in articulos:
            pedidocompdet = get_object_or_404(Pedidocompdet, pk=idpedidocompdet)
            pedidocompdet.idcompracab =float(idpedidocompcab)
            pedidocompdet.orden = orden
            pedidocompdet.idarticulo = articulo.idarticulo
            pedidocompdet.codigo =  articulo.codigo
            pedidocompdet.descripcion = articulo.descripcion
            pedidocompdet.cantidad = float(cantidad)
            pedidocompdet.unidad = articulo.unidad
            pedidocompdet.costo =articulo.costo
            pedidocompdet.precio = float(precio)
            pedidocompdet.iva = articulo.iva
            pedidocompdet.save()
            actpedidocompracab(idpedidocompcab)
            response = {'success': True}
            return JsonResponse(response)


def pedidocompdet_eliminar(request, pk_token):
    if not request.user.has_perm('compras.delete_pedidocompdet'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    pk = int(desencriptar_datos(pk_token,skey))

    objetos = Pedidocompdet.objects.filter(idpedidocompdet=pk)
    for objeto in objetos:
        idpedidocompcab= objeto.idpedidocompcab

    pedidocompdet = get_object_or_404(Pedidocompdet, pk=pk)
    pedidocompdet.delete()

    orden=0
    objetos = Pedidocompdet.objects.filter(idpedidocompcab=idpedidocompcab).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden=orden+1
        objeto.save()

    #actpedidocompracab(idpedidocompcab)
    response = {'success': True, 'message': ''}
    return JsonResponse(response)
