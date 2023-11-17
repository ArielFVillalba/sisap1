from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def hola_mundo(request):
    return HttpResponse("¡Hola Mundo en Django!")


def loginc(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            user_permissions = user.user_permissions.all()
            valor=str(user.last_login)+str(user.username)+str(user.password)
            #print(str(valor))

            # Imprime los permisos
            # for permission in user_permissions:
            #  print(permission)
            #usuario = request.user
            #user = request.user

            return render(request, 'menu.html')
        else:
            errors = "Invalid login credentials."
            return render(request, 'login.html', {'messages': errors})

    else:
        errors = ""
        if request.user.is_authenticated:
            logout(request)

        titulo= "INICIAR SESION"
    return render(request, 'login.html', {'messages': errors, 'title':titulo})


    return render(request, 'login.html', {'messages': ''})

def menu(request):
    return render(request, "menu.html")
