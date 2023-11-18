from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from .forms import *
from django.contrib import messages



def cliente_listar(request,cadena):



    if cadena == "*":

        cliente = Cliente.objects.all()
        objetos=cliente
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)

        for objeto in objetos:
            objeto.pkcl = encriptar_datos(objeto.idcliente,skey)

        return render(request, 'ventas/Cliente_listar.html', {'cliente': cliente, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'ventas/Cliente_listar.html')

    qs = Cliente.objects.filter(nombre=0)
    subcadenas = cadena.split(" ")
    for i in range(len(subcadenas)):
        qs1 = Cliente.objects.filter(nombre__icontains=subcadenas[i])
        qs = qs.union(qs1)
        qs2 = Cliente.objects.filter(direccion__icontains=subcadenas[i])
        qs = qs.union(qs2)
        qs3 = Cliente.objects.filter(cedula__icontains=subcadenas[i])
        qs = qs.union(qs3)
        qs4 = Cliente.objects.filter(ruc__icontains=subcadenas[i])
        qs = qs.union(qs4)
        qs5 = Cliente.objects.filter(telefono__icontains=subcadenas[i])
        qs = qs.union(qs5)
        qs6 = Cliente.objects.filter(timbrado__icontains=subcadenas[i])
        qs = qs.union(qs6)
        qs7 = Cliente.objects.filter(direccion__icontains=subcadenas[i])
        qs = qs.union(qs7)
        cliente = qs
        skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
        for objeto in cliente:
            objeto.pkcl = encriptar_datos(objeto.idcliente,skey)

    return render(request, 'ventas/Cliente_listar.html', {'cliente': cliente, 'cadena': cadena})


class cliente_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.view_cliente'
    model = Cliente
    form_class = ClienteForm
    template_name = 'ventas/cliente.html'
    context_object_name = 'cliente'  # Nombre para acceder al objeto en la plantilla

    def get(self, request,pk_token):

        cliente = None
        if pk_token != "0":
            skey = str(request.user.last_login) + str(request.user.username) + str(request.user.password)
            pk_desencriptado = desencriptar_datos(pk_token,skey)
            cliente = Cliente.objects.get(idcliente=int(pk_desencriptado))  # Recuperar la compra por su clave primaria



        context = {'cliente': cliente}  # Crear un diccionario de contexto
        context['title'] = '  CLIENTE  '
        context['sidr'] = '/cliente/' + str(pk_token) + '/cargar/'
        context['pkcl'] = pk_token
        context['pk_token'] = pk_token
        context['var1']= True
        context['var2']= False

        return render(request, self.template_name, context)


class cliente_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'ventas.add_cliente'
    model = Cliente
    form_class = ClienteForm
    template_name = 'ventas/Cliente.html'
    success_url = reverse_lazy('cliente_crear')

    def dispatch(self, *args, **kwargs):
        return super(cliente_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '  CREAR  CLIENTE '
        context['sidr'] = '/cliente/crear/'
        context['var1']= False
        context['var2']= True

        return context
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cliente creado exitosamente.')
        skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
        pk_encriptado = encriptar_datos(self.object.pk,skey)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('cliente_cargar', pk_token=str(pk_encriptado))


class cliente_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'ventas.change_cliente'
    model = Cliente
    form_class = ClienteForm
    template_name = 'ventas/Cliente.html'
    success_url = '/cliente/0/listar/'


    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        print(pk_token)

        if pk_token != "0":
            skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
            pk = desencriptar_datos(pk_token,skey)
            return get_object_or_404(Cliente, pk=pk)


    def get_context_data(self, **kwargs):
        pk_token = self.kwargs['pk_token']
        context = super().get_context_data(**kwargs)
        context['title'] = '  EDITAR  CLIENTE '
        context['sidr'] = '/cliente/'+ str(pk_token) + '/editar/'
        context['pkcl'] = pk_token
        context['var1']= False
        context['var2']= True
        return context

    def form_valid(self, form):
        pk_token = self.kwargs['pk_token']
        response = super().form_valid(form)
        messages.success(self.request, 'cliente editado exitosamente.')
        return redirect('cliente_cargar', pk_token=str(pk_token))


class cliente_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'ventas.delete_cliente'

    def get(self, request, pk_token):
        titulo = "¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg = " EL REGISTRO DE ClIENTE "
        if pk_token == "0":
            return redirect('cliente_cargar', pk_token=0)
        else:
            return render(request, 'base/pagcofirmacion.html', {'instance': msg, 'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        print(" CLIENTE PARA ELIMINAR " + action)

        if action == 'CONFIRMAR':
            skey = str(self.request.user.last_login) + str(self.request.user.username) + str(self.request.user.password)
            pk = desencriptar_datos(pk_token,skey)
            instance = get_object_or_404(Cliente, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            return redirect('cliente_cargar', pk_token=0)
        else:
            return redirect('cliente_cargar', pk_token=pk_token)


def cli_datos(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        # Obtenemos una lista de instancias de modelo
        #objetos = Cliente.objects.all()
        objetos = Cliente.objects.filter(idcliente=pk)
        # Convertimos cada instancia de modelo a un diccionario y los agregamos a una lista
        datos = []
        for objeto in objetos:
            datos.append({
                'idcliente': objeto.idcliente,
                'nombre': objeto.nombre,
                'ruc': objeto.ruc,
                'timbrado': objeto.timbrado,
            })

        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        Response = JsonResponse({'datos': datos})
        return Response


def cmbcli(request):
    if request.method == 'POST':
        objetos = Cliente.objects.all()
        datos = []
        for objeto in objetos:
            datos.append({
                'idcliente': objeto.idcliente,
                'nombre': objeto.nombre,
            })

        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        Response = JsonResponse({'datos': datos})
        return Response
