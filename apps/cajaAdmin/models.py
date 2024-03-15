from django.db import models

# Create your models here.

class Cupon(models.Model):
    codigo = models.CharField(max_length=30,null=True)
    porcentaje = models.FloatField(default=0,null=True)
    usado = models.BooleanField(default=False,null=True)

class Mes(models.Model):
    nombre = models.CharField(max_length=15)
    total = models.FloatField(default=0)

class Transaccion(models.Model):
    monto = models.FloatField(default=0)
    fecha = models.DateField(auto_now=True)
    hora = models.TimeField(auto_now=True)
    tipo = models.BooleanField(default=False,null=True)
    descripcion = models.CharField(max_length=50, null=True)
