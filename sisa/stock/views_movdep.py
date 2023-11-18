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



def movdepcab_filtro(request):

    return render(request, 'stock/movdep_filt.html')

def movdepcab_filtro_lst(request):
    if not request.user.is_authenticated:
        return redirect('login')

    fechaini =  request.GET.get('fechaini', '')
    fechafin =  request.GET.get('fechafin', '')
    nromov =  request.GET.get('nromov', '')

    movdepcab = Movdepcab.objects.all()


    if movdepcab.exists() and  fechaini:
            fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
            movdepcab = movdepcab.filter(fecha__gte=fecha_inicio)
    if movdepcab.exists() and  fechafin:
            fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
            movdepcab = movdepcab.filter(fecha__lte=fecha_fin)
    if movdepcab.exists() and  nromov:
            movdepcab = movdepcab.filter(nromov=nromov)

    for objeto in movdepcab:
        objeto.pkmd = encriptar_dato(objeto.idmovdepcab)
        objeto.save()

    cadena=""
    return render(request, 'stock/movdep_lst.html', {'movdepcab': movdepcab, 'cadena': cadena })


def movdepcab_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')

    if cadena == "*":
        movdepcab = Movdepcab.objects.all()
        return render(request, 'stock/movdep_lst.html', {'movdepcab': movdepcab, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'stock/movdep_lst.html')

    qs = Movdepcab.objects.filter(nombre=0)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Movdepcab.objects.filter(fecha__contains=subcadenas[i])
        qs = qs.union(qs1)
        qs2 = Movdepcab.objects.filter(nrofactura__contains=subcadenas[i])
        qs = qs.union(qs2)
        qs4 = Movdepcab.objects.filter(ruc__contains=subcadenas[i])
        qs = qs.union|(qs4)

    movdepcab = qs
    return render(request, 'stock/movdep_lst.html', {'movdepcab': movdepcab, 'cadena': cadena})


class movdepcab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'stock.view_movdepcab'
    model = Movdepcab
    form_class = MovdepcabForm
    template_name = 'stock/movdep.html'
    success_url = reverse_lazy('movdepcab_crear')

    def get(self, request,pk_token):
        movdepcab = None
        if pk_token != "0":
            pk_desencriptado = desencriptar_dato(pk_token)
            movdepcab = Movdepcab.objects.get(idmovdepcab=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'movdepcab': movdepcab}  # Crear un diccionario de contexto
        context['title'] = '  MOVIMIENTO / DEPOSITO  '
        context['sidr'] = '/compracab/' + str(pk_token) + '/cargar/'
        context['pkmb'] = pk_token
        context['pk_token'] = pk_token
        context['hab1']= True
        context['hab2']= False

        return render(request, self.template_name, context)


class movdepcab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'stock.add_movdepcab'
    model = Movdepcab
    form_class = MovdepcabForm
    template_name = 'stock/movdep.html'
    success_url = reverse_lazy('movdepcab_crear')

    def dispatch(self, *args, **kwargs):
        return super(movdepcab_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CARGAR MOV DEPOSITO '
        context['sidr'] = '/movdepcab/crear/'
        context['hab1'] = False
        context['hab2'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, ' Mov Deposito creado exitosamente.')
        response = super().form_valid(form)
        pk_encriptado = encriptar_dato(self.object.pk)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('movdepcab_cargar', pk_token=pk_encriptado)


class movdepcab_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'stock.change_movdepcab'
    model = Movdepcab
    form_class = MovdepcabForm
    template_name = 'stock/movdep.html'
    success_url = '/movdepcab/0/listar/'

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            pk = desencriptar_dato(pk_token)
            return get_object_or_404(Movdepcab, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MOVIMIENTO DE  DEPOSITO  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/movdepcab/'+str(pk_token)+'/editar/'
        context['pk_token'] = pk_token
        context['pkmd'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def get_success_url(self):
        messages.success(self.request, 'editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return reverse_lazy('movdepcab_cargar', kwargs={'pk_token': pk_token})

def movdepcab_eliminar(request, pk):
    movdepcab = get_object_or_404(Movdepcab, pk=pk)
    movdepcab.delete()
    response = {'success': True}
    return JsonResponse(response)

class movdepcab_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'compras.delete_movdepcab'

    def get(self, request, pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO DE COMPRA "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')

        if action == 'CONFIRMAR':
            pk = desencriptar_dato(pk_token)
            instance = get_object_or_404(Movdepcab, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, 'compra eliminado exitosamente.')
            return redirect('movdepcab_cargar', pk_token=0)
        else:
            return redirect('movdepcab_cargar', pk_token=pk_token)


def movdepdet_listar(request):
    if not request.user.has_perm('stock.view_movdepdet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pkmd = request.POST['pkmd']
    idmovdepcab = int(desencriptar_dato(pkmd))
    print(" idmovdepcab " + str(idmovdepcab))
    orden = request.POST['orden']

    if int(orden) == 0:
        objetos = Movdepdet.objects.filter(idmovdepcab=idmovdepcab).order_by('orden')
    if int(orden) >=1:
        objetos = Movdepdet.objects.filter(idmovdepcab=idmovdepcab,orden=orden)
    datos = []
    for objeto in objetos:
        datos.append({
            'pkmdd': encriptar_dato(objeto.idmovdepdet),
            'orden': objeto.orden,
            'codigo': objeto.codigo,
            'descripcion': objeto.descripcion,
            'cantidad': objeto.cantidad,
            'precio': objeto.precio,
            'iva': objeto.iva,
            'depsalida': objeto.depsalida,
            'depentrada': objeto.depentrada,

        })


    # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})

    return Response


def actmovdepcab(idmovdepcab):

    detalles = Movdepdet.objects.filter(iva=5,idmovdepcab=idmovdepcab)
    gravada5 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Movdepdet.objects.filter(iva=10, idmovdepcab=idmovdepcab)
    gravada10 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Movdepdet.objects.filter(iva=0, idmovdepcab=idmovdepcab)
    exenta = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    gravada=gravada10+gravada5
    total=gravada+exenta

    objetos = Movdepcab.objects.filter(idmovdepcab=idmovdepcab)
    for objeto in objetos:
        objeto.gravada5 = gravada5
        objeto.gravada10 = gravada10
        objeto.gravada = gravada
        objeto.exenta = exenta
        objeto.total = total
        objeto.save()
    return total


def movdepdet_guardar(request):
    if not request.user.has_perm('stock.add_movdepdet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    if request.method == 'POST':

        pkmd = request.POST['pkmd']
        idmovdepcab = int(desencriptar_dato(pkmd))
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        depsalida = request.POST['depsalida']
        depentrada = request.POST['depentrada']

        cantr = Movdepdet.objects.filter(idmovdepcab=idmovdepcab).count()
        cantr=cantr+1
        articulos = Articulo.objects.filter(codigo=float(codigo))
        for articulo in articulos:

            movdepdet = Movdepdet()
            movdepdet.idmovdepcab =float(idmovdepcab)
            movdepdet.orden = cantr
            movdepdet.idarticulo = articulo.idarticulo
            movdepdet.codigo =  articulo.codigo
            movdepdet.descripcion = articulo.descripcion
            movdepdet.cantidad = float(cantidad)
            movdepdet.unidad = articulo.unidad
            movdepdet.costo =articulo.costo
            movdepdet.precio = articulo.precio
            movdepdet.iva = articulo.iva
            movdepdet.depsalida = depsalida
            movdepdet.depentrada= depentrada
            movdepdet.usuario="avillalba"

            movdepdet.save()
            response = {'success': True}
            return JsonResponse(response)

def movdepdet_editar(request):
    if not request.user.has_perm('stock.change_movdepdet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    if request.method == 'POST':
        pkmd = request.POST['pkmd']
        idmovdepcab = int(desencriptar_dato(pkmd))

        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        orden = request.POST['orden']
        depsalida = request.POST['depsalida']
        depentrada = request.POST['depentrada']

        objetos = Movdepdet.objects.filter(idmovdepcab=idmovdepcab,orden=orden)
        for movdepdet in objetos:
            idmovdepdet=movdepdet.idmovdepdet

        articulos = Articulo.objects.filter(codigo=float(codigo))
        for articulo in articulos:
            movdepdet = get_object_or_404(Movdepdet, pk=idmovdepdet)
            movdepdet.idcompracab =float(idmovdepcab)
            movdepdet.orden = orden
            movdepdet.idarticulo = articulo.idarticulo
            movdepdet.codigo =  articulo.codigo
            movdepdet.descripcion = articulo.descripcion
            movdepdet.cantidad = float(cantidad)
            movdepdet.unidad = articulo.unidad
            movdepdet.costo =articulo.costo
            movdepdet.precio = articulo.precio
            movdepdet.iva = articulo.iva
            movdepdet.depsalida = depsalida
            movdepdet.depentrada= depentrada
            movdepdet.save()
            response = {'success': True}
            return JsonResponse(response)


def movdepdet_eliminar(request, pk_token):
    if not request.user.has_perm('stock.delete_movdepdet'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)

    pk = int(desencriptar_dato(pk_token))

    objetos = Movdepdet.objects.filter(idmovdepdet=pk)
    for objeto in objetos:
        idmovdepcab= objeto.idmovdepcab

    notacreditocompdet = get_object_or_404(Movdepdet, pk=pk)
    notacreditocompdet.delete()

    orden=0
    objetos = Movdepdet.objects.filter(idmovdepcab=idmovdepcab).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden=orden+1
        objeto.save()

    response = {'success': True, 'message': ''}
    return JsonResponse(response)
