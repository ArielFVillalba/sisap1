from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from compras.models import Compracab, Compradet
from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from .forms import *
from django.contrib import messages
from django.core.serializers import json
from django.db.models import Sum, F
from django.db.models import Func

con1=1
def articulos_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')

    print("ingresa en "+ cadena)
    #stockdet()
    if cadena == "*":
        articulos = Articulo.objects.all()
        for objeto in articulos:
            objeto.pka = encriptar_dato(objeto.idarticulo)
            objeto.save()
        return render(request, 'stock/articulos_listar.html', {'articulos': articulos, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'stock/articulos_listar.html')



    qs = Articulo.objects.filter(codigo=0)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Articulo.objects.filter( codigo__contains=subcadenas[i])
        qs=qs.union(qs1)
        qs2 = Articulo.objects.filter( descripcion__contains=subcadenas[i])
        qs=qs.union(qs2)
        qs3 = Articulo.objects.filter(unidad__contains=subcadenas[i])
        qs = qs.union(qs3)
        qs4 = Articulo.objects.filter(costo__contains=subcadenas[i])
        qs = qs.union(qs4)
        qs5 = Articulo.objects.filter(precio__contains=subcadenas[i])
        qs = qs.union(qs5)
        qs6 = Articulo.objects.filter(iva__contains=subcadenas[i])
        qs = qs.union(qs6)
        qs7 = Articulo.objects.filter(familia1__contains=subcadenas[i])
        qs = qs.union(qs7)
        qs8 = Articulo.objects.filter(familia2__contains=subcadenas[i])
        qs = qs.union(qs8)
        qs9 = Articulo.objects.filter(familia3__contains=subcadenas[i])
        qs = qs.union(qs9)
        qs10 = Articulo.objects.filter(familia4__contains=subcadenas[i])
        qs = qs.union(qs10)
        qs11 = Articulo.objects.filter(familia5__contains=subcadenas[i])
        qs = qs.union(qs11)
        qs12 = Articulo.objects.filter(familia6__contains=subcadenas[i])
        qs = qs.union(qs12)
        qs13 = Articulo.objects.filter(familia7__contains=subcadenas[i])
        qs = qs.union(qs13)
        articulos = qs

        for objeto in articulos:
            objeto.pka = encriptar_dato(objeto.idarticulo)
            objeto.save()

    return render(request, 'stock/articulos_listar.html', {'articulos': articulos ,'cadena': cadena})



class articulos_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'stock.view_articulo'

    model = Articulo
    form_class = ArticuloForm
    template_name = 'stock/articulo.html'
    success_url = reverse_lazy('articulos_crear')

    def get(self, request,pk_token):
        articulo = None
        if pk_token != "0":
            pk_desencriptado = desencriptar_dato(pk_token)
            articulo = Articulo.objects.get(idarticulo=int(pk_desencriptado))  # Recuperar la compra por su clave primaria

        context = {'articulo': articulo}  # Crear un diccionario de contexto
        context['title'] = '  ARTICULO  '
        context['sidr'] = '/articulo/' + str(pk_token) + '/cargar/'
        context['pka'] = pk_token
        context['pk_token'] = pk_token
        context['var1']= True
        context['var2']= False

        return render(request, self.template_name, context)


class articulos_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'stock.add_articulo'

    model = Articulo
    form_class = ArticuloForm
    template_name = 'stock/articulo.html'
    success_url = reverse_lazy('articulos_crear')

    def dispatch(self, *args, **kwargs):
        return super(articulos_crear, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '  CREAR  ARTICULO '
        context['sidr'] = '/articulos/crear/'
        context['var1']= False
        context['var2']= True
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Artículo agregado exitosamente.')
        pk_encriptado = encriptar_dato(self.object.pk)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('articulos_cargar', pk_token=str(pk_encriptado))



class articulos_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'stock.chance_articulo'

    model = Articulo
    form_class = ArticuloForm
    template_name = 'stock/articulo.html'
    success_url = reverse_lazy('articulos_editar')

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            pk = desencriptar_dato(pk_token)
            return get_object_or_404(Articulo, pk=pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] ='EDITAR  ARTICULO'
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/articulos/' + pk_token + '/editar/'
        context['pk_token'] = pk_token
        context['pka'] = pk_token
        context['var1'] = False
        context['var2'] = True
        return context

    def get_success_url(self):
        messages.success(self.request, 'articulos editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return reverse_lazy('articulos_cargar', kwargs={'pk_token': pk_token})


class articulos_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'stock.delete_articulo'

    def get(self, request, pk_token):
        titulo = "¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg = " EL REGISTRO  "
        if pk_token == "0":
            return redirect('articulos_cargar', pk_token=0)
        else:
            return render(request, 'base/pagcofirmacion.html', {'instance': msg, 'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        print(" CLIENTE PARA ELIMINAR " + action)

        if action == 'CONFIRMAR':
            pk = desencriptar_dato(pk_token)
            instance = get_object_or_404(Articulo, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            return redirect('articulos_cargar', pk_token=0)
        else:
            return redirect('articulos_cargar', pk_token=pk_token)



def cmbarticulo(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        objetos = Articulo.objects.all()
        datos = []
        for objeto in objetos:
            datos.append({
                'codigo': objeto.codigo,
                'descripcion': objeto.descripcion,
            })

        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        Response = JsonResponse({'datos': datos})
        return Response

def articulodatos(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        codigo = request.POST['codigo']
        datos=None
        if len(codigo) >2:
            objetos = Articulo.objects.filter(codigo=codigo)
            datos = []
            for objeto in objetos:
                datos.append({
                    'descripcion': objeto.descripcion,
                    'precio': objeto.precio,
                    'iva': objeto.iva,
            })

        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        Response = JsonResponse({'datos': datos})
        return Response


def articulodatosdesc(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        desc = request.POST['desc']
        datos=None
        if len(desc) >2:
            objetos = Articulo.objects.filter(descripcion__iexact=desc)
            datos = []
            for objeto in objetos:
                datos.append({
                    'codigo': objeto.codigo,
                    'descripcion': objeto.descripcion,
                    'precio': objeto.precio,
                    'iva': objeto.iva,
            })

        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        Response = JsonResponse({'datos': datos})
        return Response



def stockdet(fechaini,fechafin,codigo,deposito,sucursal):

    sql= "select *  from fc_lstexistdetalle( '"+ fechaini +"', '"+ fechafin +"','"+ codigo +"','"+ deposito +"','"+ sucursal +"');"
    #sql="select  *  from listadoview"
    valor1 = seleccionar_datos3( sql)
    print(valor1)
    return valor1

