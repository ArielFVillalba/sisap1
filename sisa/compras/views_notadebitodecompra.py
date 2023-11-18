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


def notadebitocompcab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'compras/notadebitocompra_filt.html')

def notadebitocompcab_filtro_lst(request):
    if not request.user.is_authenticated:
        return redirect('login')

    idproveedor =  request.GET.get('idproveedor', '')
    fechaini =  request.GET.get('fechaini', '')
    fechafin =  request.GET.get('fechafin', '')
    tipodoc =  request.GET.get('tipodoc', '')
    notadebitocompcab = Notadebitocompcab.objects.all()
    if idproveedor=='':
        idproveedor=0
    if notadebitocompcab.exists() and int(idproveedor) >=1:
            notadebitocompcab = notadebitocompcab.filter(idproveedor__contains=idproveedor)
    if notadebitocompcab.exists() and  fechaini:
            fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
            notadebitocompcab = notadebitocompcab.filter(fecha__gte=fecha_inicio)
    if notadebitocompcab.exists() and  fechafin:
            fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
            notadebitocompcab = notadebitocompcab.filter(fecha__lte=fecha_fin)
    if notadebitocompcab.exists() and tipodoc:
        notadebitocompcab = notadebitocompcab.filter(tipodoc=tipodoc)

    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)

    for objeto in notadebitocompcab:
        objeto.pknd = encriptar_datos(objeto.idnotadebitocompcab,skey)
    cadena=""


    return render(request, 'compras/notadebitocompra_lst.html', {'notadebitocompcab': notadebitocompcab, 'cadena': cadena })


class notadebitocompcab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'compras.view_notadebitocompcab'
    model = Notadebitocompcab
    form_class = NotadebitodecompcabForm
    template_name = 'compras/notadebitocompra.html'
    success_url = reverse_lazy('notadebitocompcab_crear')

    def get(self, request,pk_token):

        notadebitocompcab = None
        if pk_token != "0":
            skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
            pk_desencriptado = desencriptar_datos(pk_token,skey)
            notadebitocompcab = Notadebitocompcab.objects.get(idnotadebitocompcab=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'notadebitocompcab': notadebitocompcab}  # Crear un diccionario de contexto
        context['title'] = '  NOTA DEBITO - COMPRA  '
        context['sidr'] = '/notadebitocompra/' + str(pk_token) + '/cargar/'
        context['pknd'] = pk_token
        context['hab1']= True
        context['hab2']= False

        return render(request, self.template_name, context)

def notadebitocompcab_listar(request,cadena):
    if cadena == "*":

        notadebitocompcab = Notadebitocompcab.objects.all()
        return render(request, 'compras/notadebitocompra_lst.html', {'notadebitocompcab': notadebitocompcab, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'compras/notadebitocompra_lst.html')

    qs = Notadebitocompcab.objects.filter(nombre=0)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Notadebitocompcab.objects.filter(fecha__contains=subcadenas[i])
        qs = qs.union(qs1)
        qs2 = Notadebitocompcab.objects.filter(nrofactura__contains=subcadenas[i])
        qs = qs.union(qs2)
        qs3 = Notadebitocompcab.objects.filter(proveedor__contains=subcadenas[i])
        qs = qs.union(qs3)
        qs4 = Notadebitocompcab.objects.filter(ruc__contains=subcadenas[i])
        qs = qs.union|(qs4)

    notadebitocompcab = qs
    return render(request, 'compras/notadebitocompra_lst.html', {'notadebitocompcab': notadebitocompcab, 'cadena': cadena})


class notadebitocompcab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'compras.add_notadebitocompcab'

    model = Notadebitocompcab
    form_class = NotadebitodecompcabForm
    template_name = 'compras/notadebitocompra.html'
    success_url = reverse_lazy('notadebitocompcab_crear')
    def dispatch(self, *args, **kwargs):
        return super(notadebitocompcab_crear, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'NOTA DEBDITO DE COMPRA '
        context['sidr'] = '/notadebitocompcab/crear/'
        context['hab1']= False
        context['hab2']= True
        return context

    def form_valid(self,request, form):
        messages.success(self.request, ' NOTA creado exitosamente.')
        response = super().form_valid(form)
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        pk_encriptado = encriptar_datos(self.object.pk,skey)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('notadebitocompcab_cargar', pk_token=str(pk_encriptado))

class notadebitocompcab_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'compras.change_notadebitocompcab'
    model = Notadebitocompcab
    form_class = NotadebitodecompcabForm
    template_name = 'compras/notadebitocompra.html'
    success_url = '/notadebitocompcab/0/listar/'

    def get_object(self,request, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
            pk = desencriptar_dato(pk_token,skey)
            return get_object_or_404(Notadebitocompcab, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '  EDITAR NOTA  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/notadebitocompcab/' + pk_token + '/editar/'
        context['pk_token'] = pk_token
        context['pknd'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def get_success_url(self):
        compracab = self.object
        #pk_encriptado = encriptar_dato(compracab.idcompracab)  # Asegúrate de que esta función esté implementada correctamente
        messages.success(self.request, ' nota editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        #return reverse_lazy('compracab_editar', kwargs={'pk_token': pk_encriptado})
        return reverse_lazy('notadebitocompcab_cargar', kwargs={'pk_token': pk_token})


class notadebitocompcab_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'compras.delete_notadebitocompcab'

    def get(self, request, pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO DE NOTA "
        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        if action == 'CONFIRMAR':
            skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
            pk = desencriptar_datos(pk_token,skey)
            instance = get_object_or_404(Notadebitocompcab, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, 'Nota eliminado exitosamente.')
            return redirect('notadebitocompcab_cargar', pk_token=0)
        else:
            return redirect('notadebitocompcab_cargar', pk_token=pk_token)


def notadebitocompdet_listar(request):
    if not request.user.has_perm('compras.view_notadebitocompdet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pk = request.POST['pknd']
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    idnotadebitocompcab = int(desencriptar_datos(pk,skey))
    orden = request.POST['orden']


    if int(orden) == 0:
        objetos = Notadebitocompdet.objects.filter(idnotadebitocompcab=idnotadebitocompcab).order_by('orden')
    if int(orden) >=1:
        objetos = Notadebitocompdet.objects.filter(idnotadebitocompcab=idnotadebitocompcab,orden=orden)
    datos = []
    for objeto in objetos:
        datos.append({
            'pkndd': encriptar_dato(objeto.idnotadebitocompdet),
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


def actnotadebitocompracab(idnotadebitocompcab):

    #gravada10 = Compradet.objects.filter(iva=10,idcompracab=idcompracab).aggregate(total=Sum('cantidad' * 'precio'))['total']

    detalles = Notadebitocompdet.objects.filter(iva=5,idnotadebitocompcab=idnotadebitocompcab)
    gravada5 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Notadebitocompdet.objects.filter(iva=10, idnotadebitocompcab=idnotadebitocompcab)
    gravada10 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Notadebitocompdet.objects.filter(iva=0, idnotadebitocompcab=idnotadebitocompcab)
    exenta = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    gravada=gravada10+gravada5
    total=gravada+exenta

    objetos = Notadebitocompcab.objects.filter(idnotadebitocompcab=idnotadebitocompcab)
    for objeto in objetos:
        objeto.gravada5 = gravada5
        objeto.gravada10 = gravada10
        objeto.gravada = gravada
        objeto.exenta = exenta
        objeto.total = total
        objeto.save()
    return total


def notadebitocompdet_guardar(request):
    if not request.user.has_perm('compras.add_notadebitocompdet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pk = request.POST['pknd']
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)

        idnotadebitocompcab = int(desencriptar_dato(pk,skey))
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        cantr = Notadebitocompdet.objects.filter(idnotadebitocompcab=idnotadebitocompcab).count()
        cantr = cantr + 1
        articulos = Articulo.objects.filter(codigo=float(codigo))
        for articulo in articulos:
            notadebitocompdet = Notadebitocompdet()
            notadebitocompdet.idnotadebitocompcab = float(idnotadebitocompcab)
            notadebitocompdet.orden = cantr
            notadebitocompdet.idarticulo = articulo.idarticulo
            notadebitocompdet.codigo = articulo.codigo
            notadebitocompdet.descripcion = articulo.descripcion
            notadebitocompdet.cantidad = float(cantidad)
            notadebitocompdet.unidad = articulo.unidad
            notadebitocompdet.costo = articulo.costo
            notadebitocompdet.precio = float(precio)
            notadebitocompdet.iva = articulo.iva
            notadebitocompdet.save()
            actnotadebitocompracab(idnotadebitocompcab)
            response = {'success': True}
            return JsonResponse(response)


def notadebitocompdet_editar(request):
    if not request.user.has_perm('compras.change_notadebitocompdet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pk = request.POST['pknd']
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        idnotadebitocompcab = int(desencriptar_dato(pk,skey))
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        orden = request.POST['orden']


        objetos = Notadebitocompdet.objects.filter(idnotadebitocompcab=idnotadebitocompcab,orden=orden)
        for notadebitocompdet in objetos:
            idnotadebitocompdet=notadebitocompdet.idnotadebitocompdet

        articulos = Articulo.objects.filter(codigo=float(codigo))
        for articulo in articulos:
            notadebitocompdet = get_object_or_404(Notadebitocompdet, pk=idnotadebitocompdet)
            notadebitocompdet.idnotadebitocompcab =float(idnotadebitocompcab)
            notadebitocompdet.orden = orden
            notadebitocompdet.idarticulo = articulo.idarticulo
            notadebitocompdet.codigo =  articulo.codigo
            notadebitocompdet.descripcion = articulo.descripcion
            notadebitocompdet.cantidad = float(cantidad)
            notadebitocompdet.unidad = articulo.unidad
            notadebitocompdet.costo =articulo.costo
            notadebitocompdet.precio = float(precio)
            notadebitocompdet.iva = articulo.iva
            notadebitocompdet.save()
            actnotadebitocompracab(idnotadebitocompcab)
            response = {'success': True}
            return JsonResponse(response)


def notadebitocompdet_eliminar(request, pk_token):
    if not request.user.has_perm('compras.delete_notadebitocompdet'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)
    skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    pk = int(desencriptar_datos(pk_token,skey))
    objetos = Notadebitocompdet.objects.filter(idnotadebitocompdet=pk)
    for objeto in objetos:
       idnotadebitocompcab = objeto.idnotadebitocompcab

    notadebitocompdet = get_object_or_404(Notadebitocompdet, pk=pk)
    notadebitocompdet.delete()

    orden = 0
    objetos = Notadebitocompdet.objects.filter(idnotadebitocompcab=idnotadebitocompcab).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden = orden + 1
        objeto.save()

    actnotadebitocompracab(idnotadebitocompcab)
    response = {'success': True, 'message': ''}
    return JsonResponse(response)
