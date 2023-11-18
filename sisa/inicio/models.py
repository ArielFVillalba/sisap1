from django.db import models

class audit(models.Model):
    # created = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.SET_NULL)
    # user = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract=True

class auditoria(models.Model):
    usuario = models.TextField()
    fecha_hora = models.DateTimeField()
    accion = models.TextField()
    usuario = models.TextField()
    tabla = models.TextField()
    old = models.JSONField()
    new = models.JSONField()

    class Meta:
        db_table = 'auditoria'














