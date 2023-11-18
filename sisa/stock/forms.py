from django import forms
from .models import *

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['idarticulo', 'codigo', 'descripcion','unidad', 'costo', 'precio','iva','habilitado', 'muevestock',
                  'familia1', 'familia2','familia3', 'familia4', 'familia5','familia6', 'familia7'

                  ]

class DepositoForm(forms.ModelForm):
    class Meta:
        model = Deposito
        fields = '__all__'

class MovdepcabForm(forms.ModelForm):
    class Meta:
        model = Movdepcab
        fields = ['idmovdepcab', 'fecha', 'nromov','depsalida', 'depentrada','obs']

class MovdepdetForm(forms.ModelForm):
    class Meta:
        model = Movdepdet
        fields = '__all__'

class ExistenciaForm(forms.ModelForm):
    class Meta:
        model = Existencia
        fields = '__all__'
