from django.db import models

# Create your models here.

class Articulo(models.Model):
    idarticulo = models.AutoField(primary_key=True)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2 , default=0)
    precio = models.DecimalField(max_digits=20, decimal_places=2,default=0)
    iva = models.DecimalField(max_digits=4, decimal_places=0,default=0)
    familia1 = models.TextField(blank=True, null=True)
    familia2 = models.TextField(blank=True, null=True)
    familia3 = models.TextField(blank=True, null=True)
    familia4 = models.TextField(blank=True, null=True)
    familia5 = models.TextField(blank=True, null=True)
    familia6 = models.TextField(blank=True, null=True)
    familia7 = models.TextField(blank=True, null=True)
    habilitado = models.BooleanField(default=True)
    muevestock = models.BooleanField(default=True)
    pka=None

    class Meta:
        db_table = 'articulos'

class Deposito(models.Model):
    deposito = models.TextField(blank=True, null=True)
    sucursal = models.TextField()
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = 'deposito'


 #   mi_entero = models.IntegerField(min_value=0, max_value=100)

class Movdepcab(models.Model):
    idmovdepcab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nromov = models.TextField()
    depsalida = models.TextField()
    depentrada = models.TextField()
    obs = models.TextField(blank=True, null=True)
    pkmd =None
    class Meta:
        db_table = 'movdep_cab'


class Movdepdet(models.Model):
    idmovdepdet = models.AutoField(primary_key=True)
    idmovdepcab = models.DecimalField(max_digits=20, decimal_places=0)
    orden= models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.DecimalField(max_digits=20, decimal_places=0)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    depsalida= models.TextField()
    depentrada = models.TextField()
    usuario = models.TextField()
    pkmdd =None

    class Meta:
        db_table = 'movdep_det'

class Existencia(models.Model):
    codigo = models.DecimalField(max_digits=20, decimal_places=0)
    deposito = models.TextField()
    cantidad =models.DecimalField(max_digits=20, decimal_places=3)
    unidad = models.TextField()
    class Meta:
        db_table = 'existencia'
