from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def hola_mundo(request):
    return HttpResponse("¡Hola Mundo en Django!")


def loginc(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

    return render(request, 'login.html', {'messages': ''})
