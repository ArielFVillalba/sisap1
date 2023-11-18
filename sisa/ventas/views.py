from django.shortcuts import render, redirect


# Create your views here.

def menuventas(request):
    if request.user.is_authenticated:
        return render(request, "ventas/menuventas.html")
    else:
        return redirect('login')

def menucliente(request):
    if request.user.is_authenticated:
        return render(request, 'ventas/menucliente.html')
    else:
        return redirect('login')
