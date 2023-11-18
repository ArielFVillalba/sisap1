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
from django.http import Http404
from itsdangerous import URLSafeSerializer

from sisa.mixins import ValidarPermisoMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def compracab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'compras/compracab_filt.html')


def compracab_filtro_lst(request):
    if not request.user.is_authenticated:
        return redirect('login')

    print("LISTAR ")
   # listar()

    idproveedor = request.GET.get('idproveedor', '')
    fechaini = request.GET.get('fechaini', '')
    fechafin = request.GET.get('fechafin', '')
    tipodoc = request.GET.get('tipodoc', '')
    compracab = Compracab.objects.all()

    if idproveedor == '':
        idproveedor = 0
    if compracab.exists() and int(idproveedor) >= 1:
        compracab = compracab.filter(idproveedor__contains=idproveedor)
    if compracab.exists() and fechaini:
        fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
        compracab = compracab.filter(fecha__gte=fecha_inicio)
    if compracab.exists() and fechafin:
        fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
        compracab = compracab.filter(fecha__lte=fecha_fin)
    if compracab.exists() and tipodoc:
        compracab = compracab.filter(tipodoc=tipodoc)
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    for objeto in compracab:
        objeto.pkf = encriptar_datos(objeto.idcompracab,skey)

    cadena = ""
    return render(request, 'compras/compracab_listar.html', {'compracab': compracab, 'cadena': cadena})


def compracab_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')

    if cadena == "*":
        compracab = Compracab.objects.all()
        #compracab.objects.update(idcompracab=encriptar_dato(compracab.idcompracab))
        return render(request, 'compras/compracab_listar.html', {'compracab': compracab, 'cadena': cadena })

    if cadena=="0":

        return render(request, 'compras/compracab_listar.html')

    qs = Compracab.objects.filter(nombre=0)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Proveedor.objects.filter(fecha__contains=subcadenas[i])
        qs = qs.union(qs1)
        qs2 = Proveedor.objects.filter(nrofactura__contains=subcadenas[i])
        qs = qs.union(qs2)
        qs3 = Proveedor.objects.filter(proveedor__contains=subcadenas[i])
        qs = qs.union(qs3)
        qs4 = Proveedor.objects.filter(ruc__contains=subcadenas[i])
        qs = qs.union|(qs4)

    compracab = qs

    #compracab.objects.update(idcompracab=encriptar_dato(compracab.idcompracab))
    return render(request, 'compras/compracab_listar.html', {'compracab': compracab, 'cadena': cadena})


class compracab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'compras.view_compracab'
    model = Compracab
    form_class = CompracabForm
    template_name = 'compras/compracab.html'
    context_object_name = 'compracab'  # Nombre para acceder al objeto en la plantilla

    def get(self, request,pk_token):
        compracab = None
        if pk_token != "0":
            skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
            pk_desencriptado = desencriptar_datos(pk_token,skey)
            compracab = Compracab.objects.get(idcompracab=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'compracab': compracab}  # Crear un diccionario de contexto
        context['title'] = '  COMPRA  '
        context['sidr'] = '/compracab/' + str(pk_token) + '/cargar/'
        context['pkf'] = pk_token
        context['hab1']= True
        context['hab2']= False

        return render(request, self.template_name, context)


class compracab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'compras.add_compracab'
    model = Compracab
    form_class = CompracabForm
    template_name = 'compras/compracab.html'
    success_url = reverse_lazy('compracab_crear')

    def dispatch(self, *args, **kwargs):
        return super(compracab_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CARGAR COMPRA '
        context['sidr'] = '/compracab/crear/'
        context['hab1']= False
        context['hab2']= True
        return context

    def form_valid(self, form):
        messages.success(self.request, ' compra creado exitosamente.')
        response = super().form_valid(form)
        skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
        pk_encriptado = encriptar_datos(self.object.pk,skey)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('compracab_cargar', pk_token=pk_encriptado)


class compracab_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'compras.change_compracab'
    model = Compracab
    form_class = CompracabForm
    template_name = 'compras/compracab.html'


    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
            pk = desencriptar_datos(pk_token,skey)
            return get_object_or_404(Compracab, pk=pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '  EDITAR COMPRAS  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/compracab/' + pk_token + '/editar/'
        context['pk_token'] = pk_token
        context['pkf'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def get_success_url(self):
        messages.success(self.request, 'compra editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return reverse_lazy('compracab_cargar', kwargs={'pk_token': pk_token})


class CompraCabEliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'compras.delete_compracab'

    def get(self, request, pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO DE COMPRA "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')

        if action == 'CONFIRMAR':
            skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
            pk = desencriptar_datos(pk_token,skey)
            instance = get_object_or_404(Compracab, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, 'compra eliminado exitosamente.')
            return redirect('compracab_cargar', pk_token=0)
        else:
            return redirect('compracab_cargar', pk_token=pk_token)


def compradet_listar(request):
    if not request.user.has_perm('compras.view_compradet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pk = request.POST['id_pk']
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    idcompracab = int(desencriptar_datos(pk,skey))
    orden = request.POST['orden']

    if int(orden) == 0:
        objetos = Compradet.objects.filter(idcompracab=idcompracab).order_by('orden')
    if int(orden) >=1:
        objetos = Compradet.objects.filter(idcompracab=idcompracab,orden=orden)
    datos = []
    for objeto in objetos:
        datos.append({
            'pkfd': encriptar_datos(objeto.idcompradet,skey),
            'orden': objeto.orden,
            'codigo': objeto.codigo,
            'descripcion': objeto.descripcion,
            'cantidad': objeto.cantidad,
            'precio': f"{(objeto.precio):.0f}",
            'iva': f"{(objeto.iva):.0f}",
            'subtotal': f"{(objeto.precio*objeto.cantidad):.0f}"
        })

    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})
    return Response

def actcomprascab(idcompracab):

    detalles = Compradet.objects.filter(iva=5,idcompracab=idcompracab)
    gravada5 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Compradet.objects.filter(iva=10, idcompracab=idcompracab)
    gravada10 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Compradet.objects.filter(iva=0, idcompracab=idcompracab)
    exenta = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    gravada=gravada10+gravada5
    total=gravada+exenta

    objetos = Compracab.objects.filter(idcompracab=idcompracab)
    for objeto in objetos:
        objeto.gravada5 = gravada5
        objeto.gravada10 = gravada10
        objeto.gravada = gravada
        objeto.exenta = exenta
        objeto.total = total
        objeto.save()
    return total

def busdep(request):
    if request.method == 'POST':
        sql = " select codigo from stk_dep "
        usu = request.POST['usuario']
        cont = request.POST['contraseña']
        valor = seleccionar_datos("stock", sql, usu, cont)
        Response = JsonResponse({'datos': valor})
        return Response

def guardardet(request):
    if not request.user.has_perm('compras.add_compradet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pkf = request.POST['pkf']
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        idcompracab = int(desencriptar_datos(pkf,skey))
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        deposito = request.POST['deposito']

        cantr = Compradet.objects.filter(idcompracab=idcompracab).count()

        cantr=cantr+1
        articulos = Articulo.objects.filter(codigo=float(codigo))
        for articulo in articulos:
            compradet = Compradet()
            compradet.idcompracab =float(idcompracab)
            compradet.orden = cantr
            compradet.idarticulo = articulo.idarticulo
            compradet.codigo =  articulo.codigo
            compradet.descripcion = articulo.descripcion
            compradet.cantidad = float(cantidad)
            compradet.unidad = articulo.unidad
            compradet.costo =articulo.costo
            compradet.precio = float(precio)
            compradet.iva = articulo.iva
            compradet.deposito = deposito

            compradet.save()
            actcomprascab(idcompracab)
            response = {'success': True}
            return JsonResponse(response)

def compradetmod(request):
    if not request.user.has_perm('compras.change_compradet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pkf = request.POST['pkf']
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        idcompracab = int(desencriptar_datos(pkf,skey))
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        orden = request.POST['orden']
        deposito = request.POST['deposito']

        objetos = Compradet.objects.filter(idcompracab=idcompracab,orden=orden)
        for compradet in objetos:
            idcompradet=compradet.idcompradet

        articulos = Articulo.objects.filter(codigo=float(codigo))

        for articulo in articulos:
            compradet = get_object_or_404(Compradet, pk=idcompradet)
            compradet.idcompracab =float(idcompracab)
            compradet.orden = orden
            compradet.idarticulo = articulo.idarticulo
            compradet.codigo =  articulo.codigo
            compradet.descripcion = articulo.descripcion
            compradet.cantidad = float(cantidad)
            compradet.unidad = articulo.unidad
            compradet.costo =articulo.costo
            compradet.precio = float(precio)
            compradet.iva = articulo.iva
            compradet.deposito = deposito
            compradet.save()
            actcomprascab(idcompracab)
            response = {'success': True}
            return JsonResponse(response)



def compradet_eliminar(request, pk_token):
    if not request.user.has_perm('compras.delete_compradet'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    pk = int(desencriptar_datos(pk_token,skey))
    objetos = Compradet.objects.filter(idcompradet=pk)
    for objeto in objetos:
        idcompracab= objeto.idcompracab

    compradet = get_object_or_404(Compradet, pk=pk)
    compradet.delete()

    orden=0
    objetos = Compradet.objects.filter(idcompracab=idcompracab).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden=orden+1
        objeto.save()

    actcomprascab(idcompracab)
    response = {'success': True, 'message': ''}
    return JsonResponse(response)
