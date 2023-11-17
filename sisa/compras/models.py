
from django.db import models


class Proveedor(models.Model):
    idproveedor = models.AutoField(primary_key=True)
    nombre = models.TextField()
    cedula = models.TextField(blank=True, null=True)
    fechanac = models.DateField(blank=True, null=True)
    ruc = models.TextField(blank=True, null=True)
    timbrado = models.TextField(blank=True, null=True)
    telefono = models.TextField(blank=True, null=True)
    mail = models.TextField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    ciudad = models.TextField(blank=True, null=True)

    pkpr = None

    class Meta:
        db_table = 'proveedor'

        def __str__(self):
            return self.cedula




class Compracab(models.Model):
    idcompracab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nrofactura = models.TextField()
    idproveedor = models.DecimalField(max_digits=20, decimal_places=0)
    proveedor = models.TextField()
    ruc = models.TextField()
    timbrado = models.TextField()
    tipodoc = models.TextField()
    condicion = models.TextField(blank=True, null=True)
    fechavto = models.DateField(blank=True, null=True)
    fecharece = models.DateField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    gravada5 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada10 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    exenta = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    deposito = models.TextField(blank=True, null=True)
    moneda = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pkf = None

    class Meta:
        db_table = 'compra_cab'


class Compradet(models.Model):
    idcompradet = models.AutoField(primary_key=True)
    idcompracab = models.DecimalField(max_digits=20, decimal_places=0)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.DecimalField(max_digits=20, decimal_places=0)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    deposito = models.TextField(blank=True, null=True)
    pkfd = None

    class Meta:
        db_table = 'compra_det'


class Comprascuotas(models.Model):
    idcomprascuotas = models.AutoField(primary_key=True)
    idcompracab = models.DecimalField(max_digits=20, decimal_places=0)
    idproveedor = models.DecimalField(max_digits=20, decimal_places=0)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    fechavto = models.DateField()
    monto = models.DecimalField(max_digits=12, decimal_places=3)
    saldo = models.DecimalField(max_digits=12, decimal_places=3)
    moneda = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        db_table = 'comprascuotas'


class Pagoproveedor(models.Model):
    idpagoproveedor = models.AutoField(primary_key=True)
    fecha = models.DateField()
    recibo = models.TextField()
    idproveedor = models.DecimalField(max_digits=20, decimal_places=0)
    proveedor = models.TextField()

    class Meta:
        db_table = 'pagoproveedor'

class Pagoprovforma(models.Model):
    idpagoprovforma = models.AutoField(primary_key=True)
    idpagoproveedor = models.DecimalField(max_digits=20, decimal_places=0)
    idtipopago = models.DecimalField(max_digits=20, decimal_places=0)
    fecha = models.DateField()
    banco  = models.TextField()
    ctacte  = models.TextField()
    nrodoc  = models.TextField()
    idproveedor = models.DecimalField(max_digits=20, decimal_places=0)
    monto = models.DecimalField(max_digits=12, decimal_places=3)
    moneda = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        db_table = 'pagoprovforma'

class Pagoprovfact(models.Model):
    idpagoprovfact = models.AutoField(primary_key=True)
    idpagoproveedor = models.DecimalField(max_digits=20, decimal_places=0)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idcomprascuotas = models.DecimalField(max_digits=20, decimal_places=0)
    fecha = models.DateField()
    saldo = models.DecimalField(max_digits=12, decimal_places=3)
    monto = models.DecimalField(max_digits=12, decimal_places=3)

    class Meta:
        db_table = 'pagoprovfact'





class Ordencompcab(models.Model):
    idordencompcab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nroorden = models.TextField()
    idproveedor = models.DecimalField(max_digits=20, decimal_places=0)
    proveedor = models.TextField()
    ruc = models.TextField()
    timbrado = models.TextField()
    tipodoc = models.TextField()
    condicion = models.TextField(blank=True, null=True)
    fechavto = models.DateField(blank=True, null=True)
    fecharece = models.DateField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    gravada5 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada10 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    exenta = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    moneda = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    pkf = None

    class Meta:
        db_table = 'ordencomp_cab'


class Ordencompdet(models.Model):
    idordencompdet = models.AutoField(primary_key=True)
    idordencompcab = models.DecimalField(max_digits=20, decimal_places=0)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.DecimalField(max_digits=20, decimal_places=0)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    pkfd = None

    class Meta:
        db_table = 'ordencomp_det'


class Pedidocompcab(models.Model):
    idpedidocompcab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nropedido = models.TextField()
    idproveedor = models.DecimalField(max_digits=20, decimal_places=0)
    proveedor = models.TextField()
    ruc = models.TextField()
    timbrado = models.TextField()
    tipodoc = models.TextField()
    condicion = models.TextField(blank=True, null=True)
    fechavto = models.DateField(blank=True, null=True)
    fecharece = models.DateField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    gravada5 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada10 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    exenta = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    moneda = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    pkpc = None

    class Meta:
        db_table = 'pedidocomp_cab'


class Pedidocompdet(models.Model):
    idpedidocompdet = models.AutoField(primary_key=True)
    idpedidocompcab = models.DecimalField(max_digits=20, decimal_places=0)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.DecimalField(max_digits=20, decimal_places=0)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    pkpcd = None

    class Meta:
        db_table = 'pedidocomp_det'


class Presupuestocompcab(models.Model):
    idpresupuestocompcab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nropresupuesto = models.TextField()
    idproveedor = models.DecimalField(max_digits=20, decimal_places=0)
    proveedor = models.TextField()
    ruc = models.TextField()
    timbrado = models.TextField()
    tipodoc = models.TextField()
    condicion = models.TextField(blank=True, null=True)
    fechavto = models.DateField(blank=True, null=True)
    fecharece = models.DateField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    gravada5 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada10 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    exenta = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    moneda = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    pkpc = None

    class Meta:
        db_table = 'presupestocomp_cab'


class Presupuestocompdet(models.Model):
    idpresupuestocompdet = models.AutoField(primary_key=True)
    idpresupuestocompcab = models.DecimalField(max_digits=20, decimal_places=0)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.DecimalField(max_digits=20, decimal_places=0)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    pkpcd = None

    class Meta:
        db_table = 'presupuestocomp_det'


class Notacreditocompcab(models.Model):
    idnotacreditocompcab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nronota = models.TextField()
    idproveedor = models.DecimalField(max_digits=20, decimal_places=0)
    proveedor = models.TextField()
    ruc = models.TextField()
    timbrado = models.TextField()
    tipodoc = models.TextField()
    condicion = models.TextField(blank=True, null=True)
    fechavto = models.DateField(blank=True, null=True)
    fecharece = models.DateField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    gravada5 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada10 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    exenta = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    deposito = models.TextField(blank=True, null=True)
    moneda = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)


    pknc = None

    class Meta:
        db_table = 'notacreditocomp_cab'


class Notacreditocompdet(models.Model):
    idnotacreditocompdet = models.AutoField(primary_key=True)
    idnotacreditocompcab = models.DecimalField(max_digits=20, decimal_places=0)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.DecimalField(max_digits=20, decimal_places=0)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    deposito = models.TextField(blank=True, null=True)
    pkncd = None

    class Meta:
        db_table = 'notacreditocomp_det'


class Notadebitocompcab(models.Model):
    idnotadebitocompcab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nrodebito = models.TextField()
    idproveedor = models.DecimalField(max_digits=20, decimal_places=0)
    proveedor = models.TextField()
    ruc = models.TextField()
    timbrado = models.TextField()
    tipodoc = models.TextField()
    condicion = models.TextField(blank=True, null=True)
    fechavto = models.DateField(blank=True, null=True)
    fecharece = models.DateField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    gravada5 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada10 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    exenta = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    moneda = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    pknd = None

    class Meta:
        db_table = 'notadebitocomp_cab'


class Notadebitocompdet(models.Model):
    idnotadebitocompdet = models.AutoField(primary_key=True)
    idnotadebitocompcab = models.DecimalField(max_digits=20, decimal_places=0)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.DecimalField(max_digits=20, decimal_places=0)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    pkndd = None

    class Meta:
        db_table = 'notadebitocomp_det'
