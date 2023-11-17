from django.urls import path
from .views import *

urlpatterns = [
    path('hola/', hola_mundo, name='hola_mundo'),
    path('login/', loginc, name='login'),
    path('menu/', menu, name='menu'),

]
