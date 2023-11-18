
from django.contrib import admin
from django.urls import path
from compras import views
from stock.views_stock_lst import *


urlpatterns = [
    path('stock/', stock, name='stock'),
    path('stockinf_listar/', stockinf_listar, name='stockinf_listar'),
    path('stockinfpdf/', stockinfpdf, name="stockinfpdf"),
    path('stockinfexcel/', stockinfexcel, name="stockinfexcel"),
    path('stockinfcsv/', stockinfcsv, name="stockinfcsv"),

    path('stockdetinf_listar/', stockdetinf_listar, name="stockdetinf_listar"),
    path('stockdetinfpdf/', stockdetinfpdf, name="stockdetinfpdf"),
    path('stockdetinfexcel/', stockdetinfexcel, name="stockdetinfexcel"),
    path('stockdetinfcsv/', stockdetinfcsv, name="stockdetinfcsv"),






]