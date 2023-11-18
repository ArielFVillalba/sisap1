from django.db import models

# Create your models here.



class Cliente(models.Model):
    idcliente= models.AutoField(primary_key=True)
    nombre = models.TextField()
    cedula = models.TextField(blank=True, null=True)
    fechanac = models.DateField(blank=True, null=True)
    ruc = models.TextField(blank=True, null=True)
    timbrado = models.TextField(blank=True, null=True)
    telefono = models.TextField(blank=True, null=True)
    mail = models.TextField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    ciudad = models.TextField(blank=True, null=True)
    pkcl= None

    class Meta:
        db_table = 'cliente'


class Ventacab(models.Model):
    idventacab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nrofactura = models.TextField()
    idcliente = models.DecimalField(max_digits=20, decimal_places=0)
    cliente= models.TextField()
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

    pkf=None

    class Meta:
        db_table = 'venta_cab'

class Ventadet(models.Model):
    idventadet = models.AutoField(primary_key=True)
    idventacab = models.DecimalField(max_digits=20, decimal_places=0)
    orden= models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.DecimalField(max_digits=20, decimal_places=0)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    deposito = models.TextField(blank=True, null=True)

    pkfd=None

    class Meta:
        db_table = 'venta_det'



class Ventascuotas(models.Model):
    idventascuotas = models.AutoField(primary_key=True)
    idventacab = models.DecimalField(max_digits=20, decimal_places=0)
    idcliente = models.DecimalField(max_digits=20, decimal_places=0)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    fechavto = models.DateField()
    monto = models.DecimalField(max_digits=12, decimal_places=3)
    saldo = models.DecimalField(max_digits=12, decimal_places=3)
    moneda = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        db_table = 'ventascuotas'


class Pagoclientes(models.Model):
    idpagocliente = models.AutoField(primary_key=True)
    fecha = models.DateField()
    recibo = models.TextField()
    idcliente = models.DecimalField(max_digits=20, decimal_places=0)
    cliente = models.TextField()
    class Meta:
        db_table = 'pagocliente'


class Pagocliforma(models.Model):
    idpagocliforma = models.AutoField(primary_key=True)
    idpagocliente = models.DecimalField(max_digits=20, decimal_places=0)
    idtipopago = models.DecimalField(max_digits=20, decimal_places=0)
    fecha = models.DateField()
    banco  = models.TextField()
    ctacte  = models.TextField()
    nrodoc  = models.TextField()
    idcliente = models.DecimalField(max_digits=20, decimal_places=0)
    monto = models.DecimalField(max_digits=12, decimal_places=3)
    moneda = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        db_table = 'pagopcliforma'

class Pagoclifact(models.Model):
    idpagoclifact = models.AutoField(primary_key=True)
    idpagocliente = models.DecimalField(max_digits=20, decimal_places=0)
    idventascuotas = models.DecimalField(max_digits=20, decimal_places=0)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    fecha = models.DateField()
    saldo = models.DecimalField(max_digits=12, decimal_places=3)
    monto = models.DecimalField(max_digits=12, decimal_places=3)

    class Meta:
        db_table = 'pagoclifact'



class Ordenventacab(models.Model):
    idordenventacab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nroorden = models.TextField()
    idcliente= models.DecimalField(max_digits=20, decimal_places=0)
    cliente= models.TextField()
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
    pkov=None

    class Meta:
        db_table = 'ordenventa_cab'

class Ordenventadet(models.Model):
    idordenventadet = models.AutoField(primary_key=True)
    idordenventacab = models.DecimalField(max_digits=20, decimal_places=0)
    orden= models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.DecimalField(max_digits=20, decimal_places=0)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    pkovd=None

    class Meta:
        db_table = 'ordenventa_det'





class Pedidoventacab(models.Model):
    idpedidoventacab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nropedido = models.TextField()
    idcliente= models.DecimalField(max_digits=20, decimal_places=0)
    cliente= models.TextField()
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
    pkpv =None

    class Meta:
        db_table = 'pedidoventa_cab'

class Pedidoventadet(models.Model):
    idpedidoventadet = models.AutoField(primary_key=True)
    idpedidoventacab = models.DecimalField(max_digits=20, decimal_places=0)
    orden= models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.DecimalField(max_digits=20, decimal_places=0)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    pkpvd = None
    class Meta:
        db_table = 'pedidoventa_det'


class Presupuestoventacab(models.Model):
    idpresupuestoventacab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nropresupuesto = models.TextField()
    idcliente= models.DecimalField(max_digits=20, decimal_places=0)
    cliente= models.TextField()
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
    pkpv= None

    class Meta:
        db_table = 'presupestoventa_cab'

class Presupuestoventadet(models.Model):
    idpresupuestoventadet = models.AutoField(primary_key=True)
    idpresupuestoventacab = models.DecimalField(max_digits=20, decimal_places=0)
    orden= models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.DecimalField(max_digits=20, decimal_places=0)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    pkpvd= None

    class Meta:
        db_table = 'presupuestoventa_det'

class Notacreditoventacab(models.Model):
    idnotacreditoventacab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nronota = models.TextField()
    idcliente= models.DecimalField(max_digits=20, decimal_places=0)
    cliente= models.TextField()
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

    pknc=None
    class Meta:
        db_table = 'notacreditoventa_cab'

class Notacreditoventadet(models.Model):
    idnotacreditoventadet = models.AutoField(primary_key=True)
    idnotacreditoventacab = models.DecimalField(max_digits=20, decimal_places=0)
    orden= models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.DecimalField(max_digits=20, decimal_places=0)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    deposito = models.TextField(blank=True, null=True)

    pkncd=None

    class Meta:
        db_table = 'notacreditoventa_det'

class Notadebitoventacab(models.Model):
    idnotadebitoventacab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nrodebito = models.TextField()
    idcliente= models.DecimalField(max_digits=20, decimal_places=0)
    cliente= models.TextField()
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
    pknd=None

    class Meta:
        db_table = 'notadebitoventa_cab'

class Notadebitoventadet(models.Model):
    idnotadebitoventadet = models.AutoField(primary_key=True)
    idnotadebitoventacab = models.DecimalField(max_digits=20, decimal_places=0)
    orden= models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.DecimalField(max_digits=20, decimal_places=0)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    pkndd =None
    class Meta:
        db_table = 'notadebitoventa_det'

