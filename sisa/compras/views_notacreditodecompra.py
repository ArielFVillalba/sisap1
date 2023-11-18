from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import datetime
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.datetime_safe import datetime

from compras.forms import NotacreditodecompcabForm
from compras.models import *
from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from django.contrib import messages
from django.core.serializers import json
from django.db.models import Sum



def notacreditocompcab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'compras/notacreditocompra_filt.html')

def notacreditocompcab_filtro_lst(request):
    if not request.user.is_authenticated:
        return redirect('login')

    idproveedor = request.GET.get('idproveedor', '')
    fechaini = request.GET.get('fechaini', '')
    fechafin = request.GET.get('fechafin', '')
    tipodoc = request.GET.get('tipodoc', '')


    notacreditocompcab = Notacreditocompcab.objects.all()
    objetos = notacreditocompcab

    if idproveedor == '':
        idproveedor = 0
    if notacreditocompcab.exists() and int(idproveedor) >= 1:
        notacreditocompcab = notacreditocompcab.filter(idproveedor__contains=idproveedor)
    if notacreditocompcab.exists() and fechaini:
        fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
        notacreditocompcab = notacreditocompcab.filter(fecha__gte=fecha_inicio)
    if notacreditocompcab.exists() and fechafin:
        fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
        notacreditocompcab = notacreditocompcab.filter(fecha__lte=fecha_fin)
    if notacreditocompcab.exists() and tipodoc:
        notacreditocompcab = notacreditocompcab.filter(tipodoc=tipodoc)
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)

    for objeto in notacreditocompcab:
        objeto.pknc = encriptar_datos(objeto.idnotacreditocompcab,skey)

    cadena=""
    return render(request, 'compras/notacreditocompra_lst.html', {'notacreditocompcab': notacreditocompcab, 'cadena': cadena })


def notacreditocompcab_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')

    if cadena == "*":
        notacreditocompcab = Notacreditocompcab.objects.all()
        return render(request, 'compras/notacreditocompra_lst.html', {'notacreditocompcab': notacreditocompcab, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'compras/notacreditocompra_lst.html')

    qs = Notacreditocompcab.objects.filter(nombre=0)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Notacreditocompcab.objects.filter(fecha__contains=subcadenas[i])
        qs = qs.union(qs1)
        qs2 = Notacreditocompcab.objects.filter(nrofactura__contains=subcadenas[i])
        qs = qs.union(qs2)
        qs3 = Notacreditocompcab.objects.filter(proveedor__contains=subcadenas[i])
        qs = qs.union(qs3)
        qs4 = Notacreditocompcab.objects.filter(ruc__contains=subcadenas[i])
        qs = qs.union|(qs4)

    notacreditocompcab = qs
    return render(request, 'compras/notacreditodecompra_lst.html', {'notacreditocompcab': notacreditocompcab, 'cadena': cadena})


class notacreditocompcab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'compras.view_notacreditocompcab'
    model = Notacreditocompcab
    form_class = NotacreditodecompcabForm
    template_name = 'compras/notacreditocompra.html'
    context_object_name = 'notacreditocompra'  # Nombre para acceder al objeto en la plantilla

    def get(self, request,pk_token):
        if not request.user.is_authenticated:
            print(" not permission notacreditocompcab_cargar")
        else:
            print(" si  permission notacreditocompcab_cargar")

        notacreditocompcab = None
        if pk_token != "0":
            skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
            pk_desencriptado = desencriptar_datos(pk_token,skey)
            notacreditocompcab = Notacreditocompcab.objects.get(idnotacreditocompcab=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'notacreditocompcab': notacreditocompcab}  # Crear un diccionario de contexto
        context['title'] = '  NOTA CREDITO DE COMPRA   '
        context['sidr'] = '/notacreditocompcab/' + str(pk_token) + '/cargar/'
        context['pknc'] = pk_token
        context['hab1']= True
        context['hab2']= False

        return render(request, self.template_name, context)

class notacreditocompcab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'compras.add_notacreditocompcab'
    model = Notacreditocompcab
    form_class = NotacreditodecompcabForm
    template_name = 'compras/notacreditocompra.html'
    success_url = reverse_lazy('notacreditocompcab_crear')
    def dispatch(self, *args, **kwargs):
        return super(notacreditocompcab_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CARGAR NOTA '
        context['sidr'] = '/notacreditocompcab/crear/'
        context['hab1']= False
        context['hab2']= True
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'creado exitosamente.')
        skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
        pk_encriptado = encriptar_datos(self.object.pk,skey)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('notacreditocompcab_cargar', pk_token=pk_encriptado)

class notacreditocompcab_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'compras.change_notacreditocompcab'

    model = Notacreditocompcab
    form_class = NotacreditodecompcabForm
    template_name = 'compras/notacreditocompra.html'
    success_url = '/notacreditocompcab/0/listar/'

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
            pk = desencriptar_datos(pk_token,skey)
            return get_object_or_404(Notacreditocompcab, pk=pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '  EDITAR NOTA  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/notacreditocompcab/' + pk_token + '/editar/'
        context['pk_token'] = pk_token
        context['pknc'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def get_success_url(self):
        messages.success(self.request, ' editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return reverse_lazy('notacreditocompcab_cargar', kwargs={'pk_token': pk_token})


class notacreditocompcab_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'compras.delete_notacreditocompcab'

    def get(self, request, pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO DE COMPRA "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        if action == 'CONFIRMAR':
            skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
            pk = desencriptar_datos(pk_token,skey)
            instance = get_object_or_404(Notacreditocompcab, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, 'registro eliminado exitosamente.')
            return redirect('notacreditocompcab_cargar', pk_token=0)
        else:
            return redirect('notacreditocompcab_cargar', pk_token=pk_token)


def notacreditocompdet_listar(request):
    if not request.user.has_perm('compras.view_notacreditocompdet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pk = request.POST['pknc']
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    idnotacreditocompcab = int(desencriptar_datos(pk,skey))
    orden = request.POST['orden']

    if int(orden) == 0:
        objetos = Notacreditocompdet.objects.filter(idnotacreditocompcab=idnotacreditocompcab).order_by('orden')
    if int(orden) >=1:
        objetos = Notacreditocompdet.objects.filter(idnotacreditocompcab=idnotacreditocompcab,orden=orden)
    datos = []
    for objeto in objetos:
        datos.append({
            'pkncd': encriptar_datos(objeto.idnotacreditocompdet,skey),
            'orden': objeto.orden,
            'codigo': objeto.codigo,
            'descripcion': objeto.descripcion,
            'cantidad': objeto.cantidad,
            'precio': f"{(objeto.precio):.0f}",
            'iva': f"{(objeto.iva):.0f}",
            'subtotal': f"{(objeto.precio*objeto.cantidad):.0f}"
        })

    # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})
    return Response


def actnotacreditocompracab(idnotacreditocompcab):

    #gravada10 = Compradet.objects.filter(iva=10,idcompracab=idcompracab).aggregate(total=Sum('cantidad' * 'precio'))['total']

    detalles = Notacreditocompdet.objects.filter(iva=5,idnotacreditocompcab=idnotacreditocompcab)
    gravada5 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Notacreditocompdet.objects.filter(iva=10, idnotacreditocompcab=idnotacreditocompcab)
    gravada10 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Notacreditocompdet.objects.filter(iva=0, idnotacreditocompcab=idnotacreditocompcab)
    exenta = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    gravada=gravada10+gravada5
    total=gravada+exenta

    objetos = Notacreditocompcab.objects.filter(idnotacreditocompcab=idnotacreditocompcab)
    for objeto in objetos:
        objeto.gravada5 = gravada5
        objeto.gravada10 = gravada10
        objeto.gravada = gravada
        objeto.exenta = exenta
        objeto.total = total
        objeto.save()
    return total


def notacreditocompdet_guardar(request):
    if not request.user.has_perm('compras.add_notacreditocompdet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pk = request.POST['pknc']
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        idnotacreditocompcab = int(desencriptar_datos(pk,skey))
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        deposito = request.POST['deposito']

        cantr = Notacreditocompdet.objects.filter(idnotacreditocompcab=idnotacreditocompcab).count()

        cantr=cantr+1
        articulos = Articulo.objects.filter(codigo=float(codigo))
        for articulo in articulos:
            notacreditocompdet = Notacreditocompdet()
            notacreditocompdet.idnotacreditocompcab =float(idnotacreditocompcab)
            notacreditocompdet.orden = cantr
            notacreditocompdet.idarticulo = articulo.idarticulo
            notacreditocompdet.codigo =  articulo.codigo
            notacreditocompdet.descripcion = articulo.descripcion
            notacreditocompdet.cantidad = float(cantidad)
            notacreditocompdet.unidad = articulo.unidad
            notacreditocompdet.costo =articulo.costo
            notacreditocompdet.precio = float(precio)
            notacreditocompdet.iva = articulo.iva
            notacreditocompdet.deposito = deposito

            notacreditocompdet.save()
            actnotacreditocompracab(idnotacreditocompcab)
            response = {'success': True}
            return JsonResponse(response)

def notacreditocompdet_editar(request):
    if not request.user.has_perm('compras.change_notacreditocompdet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pknc = request.POST['pknc']
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        idnotacreditocompcab = int(desencriptar_datos(pknc,skey))
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        orden = request.POST['orden']
        deposito = request.POST['deposito']

        objetos = Notacreditocompdet.objects.filter(idnotacreditocompcab=idnotacreditocompcab,orden=orden)
        for notacreditocompdet in objetos:
            idnotacreditocompdet=notacreditocompdet.idnotacreditocompdet

        articulos = Articulo.objects.filter(codigo=float(codigo))
        for articulo in articulos:
            notacreditocompdet = get_object_or_404(Notacreditocompdet, pk=idnotacreditocompdet)
            notacreditocompdet.idnotacreditocompcab =float(idnotacreditocompcab)
            notacreditocompdet.orden = orden
            notacreditocompdet.idarticulo = articulo.idarticulo
            notacreditocompdet.codigo =  articulo.codigo
            notacreditocompdet.descripcion = articulo.descripcion
            notacreditocompdet.cantidad = float(cantidad)
            notacreditocompdet.unidad = articulo.unidad
            notacreditocompdet.costo =articulo.costo
            notacreditocompdet.precio = float(precio)
            notacreditocompdet.iva = articulo.iva
            notacreditocompdet.deposito = deposito

            notacreditocompdet.save()
            actnotacreditocompracab(idnotacreditocompcab)
            response = {'success': True}
            return JsonResponse(response)



def notacreditocompdet_eliminar(request, pk_token):
    if not request.user.has_perm('compras.delete_notacreditocompdet'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    pk = int(desencriptar_datos(pk_token,skey))

    objetos = Notacreditocompdet.objects.filter(idnotacreditocompdet=pk)
    for objeto in objetos:
        idnotacreditocompcab= objeto.idnotacreditocompcab

    notacreditocompdet = get_object_or_404(Notacreditocompdet, pk=pk)
    notacreditocompdet.delete()

    orden=0
    objetos = Notacreditocompdet.objects.filter(idnotacreditocompcab=idnotacreditocompcab).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden=orden+1
        objeto.save()

    actnotacreditocompracab(idnotacreditocompcab)
    response = {'success': True, 'message': ''}
    return JsonResponse(response)
