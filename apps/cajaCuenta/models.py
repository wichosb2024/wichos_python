from django.db import models
from django.contrib.auth.models import User
from decimal import *

# Create your models here.

# Insumo, Mesa
# CategoriaProducto, Producto, ProductoInsumo
# Cuenta,Pedido, LineaDePedido,ProductoLinea

class Insumo(models.Model):
    nombreIns = models.CharField(max_length=30,default=" ")
    cantPaquete = models.IntegerField(default=1)
    proveedor = models.CharField(max_length=30,null=True)
    paquete = models.BooleanField(default=False)
    def __str__(self):
       return '%s'%(self.nombreIns)

class Existencia(models.Model):
    fkInsumo= models.ForeignKey(Insumo,on_delete=models.CASCADE,null=True)
    cantidad = models.IntegerField(default=0)
    def disminuir(self, valor):
        self.cantidad=self.cantidad - valor
    def aumentar(self, valor):
        self.cantidad=self.cantidad + valor
    def __str__(self):
        return '%s'%(self.fkInsumo.nombreIns + "  " + str(self.cantidad))
class Receta(models.Model):
    nombre = models.CharField(max_length=50, default= " ")
    def __str__(self):
       return '%s'%(self.nombre)
class LineaDeReceta(models.Model):
    fkInsumo=models.ForeignKey(Insumo, on_delete=models.CASCADE,null=True)
    fkReceta=models.ForeignKey(Receta, null=True, on_delete=models.CASCADE)
    cantidad=models.IntegerField(default=1)
    def __str__(self):
        return '%s'%(self.fkInsumo.nombreIns)
        


class Mesa(models.Model):
    disponible = models.BooleanField(default=True)
    def __str__(self):
       return '%i'%(self.id)
    def setDisponible(self,valor):
        self.disponible=valor

class CategoriaProducto(models.Model):
    nombreCate = models.CharField(max_length=30)
    comidaMexicana=models.BooleanField(default=False)
    cocinaNormal=models.BooleanField(default=False)
    def __str__(self):
       return '%s'%(self.nombreCate)

class Producto(models.Model):
    nombreProd = models.CharField(max_length=30)
    abreviatura = models.CharField(max_length=30,null=True,blank=True)
    precio = models.DecimalField(max_digits=4,decimal_places=2,default=0)
    fkCategoriaProducto = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE,null=True)
    receta = models.ForeignKey(Receta,on_delete=models.CASCADE,null=True)
    cebolla = models.BooleanField(default=False)
    aguacate = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='media',blank=True)
    def __unicode__(self, ):
        return str(self.image)
    def __str__(self):
       return '%s'%(self.nombreProd)
   

class Cuenta(models.Model):
    visible = models.BooleanField(default = False)
    telefono = models.CharField(max_length=8,default=00000000)
    comentario= models.CharField(null=True,max_length=300)
    archivado = models.BooleanField(default=False)
    naturaleza =models.BooleanField(default=False)
    final = models.BooleanField(default=False)
    aunEnCocina = models.BooleanField(default=True)
    impreso = models.BooleanField(default=False)
    delivery=models.BooleanField(default=False)
    direccion = models.CharField(default="", max_length=50)
    fkMesero = models.CharField(max_length=30, null=True, blank=True)
    fkCajero = models.CharField(max_length=30, null=True, blank=True)
    cliente = models.CharField(max_length=30, null=True, blank=True)
    total = models.FloatField(null=True,default=0)
    modificado = models.BooleanField(default=False)
    cancelado= models.BooleanField(default=False)
    fkMesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, null=True,blank=True)
    fechaCuenta = models.DateField(auto_now=False,auto_now_add=True,null=True)
    horaCuenta = models.TimeField(auto_now=False,auto_now_add=True,null=True)
    def setDelivery(self,valor):
        self.delivery=valor
    def setDireccion(self,valor):
        self.direccion=valor
    def setCliente(self,valor):
        self.cliente=valor
    def setMesa(self,valor):
        self.fkMesa=valor
    def setVendedor(self,valor):
        self.fkVendedor=valor
    def setImpreso(self,valor):
        self.impreso=valor
    def setTotal(self,valor):
        self.total=self.total + valor
    def setArchivado(self,valor):
        self.archivado=valor
    def setFinal(self,valor):
        self.final=valor
    def setAunEnCocina(self,valor):
        self.aunEnCocina=valor
    def descuento(self,valor):
        self.total=self.total - ((valor/100)*self.total)
        self.total=round(self.total,2)
    


class Pedido(models.Model):
    cobrado=models.BooleanField(default=False)
    exito= models.BooleanField(default=False)
    cancelado = models.BooleanField(default=False)
    subtotal = models.FloatField(null=True,default=0)
    display = models.BooleanField(default=False)
    prioridad = models.BooleanField(default=False)
    fkCuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE,null=True)
    paraLlevar = models.BooleanField(default=False)
    modificado = models.BooleanField(default=False)
    fkMesero = models.CharField(max_length=30, null=True, blank=True)
    comentariomod = models.CharField(null=True, blank=True, max_length=300)
    enCocina = models.BooleanField(default=False)
    comentarios=models.CharField(null=True,blank=True,max_length=140)
    horaPedido = models.TimeField(auto_now=False,auto_now_add=True,null=True)
    tyh     = models.BooleanField(default=False)
    mex     = models.BooleanField(default=False)

    def setParaLlevar(self,valor):
        self.paraLlevar=valor
    def setFK(self, valor):
        self.fkCuenta=valor
        self.save()
    def getFkCuenta(self):
        return self.fkCuenta
    def setComentario(self,valor):
        self.comentarios=valor
    def setPrioridad(self,valor):
        self.prioridad=valor
    def setCocina(self,valor):
        self.enCocina=valor
    def getCocina(self):
        return self.enCocina
    def setDisplay(self):
        self.display=True

class LineaDePedido(models.Model):
    comentarioMod = models.CharField(max_length=100,blank=True,null=True)
    cancelado = models.BooleanField(default=False)
    modificado = models.BooleanField(default=False)
    fkPedido = models.ForeignKey(Pedido, on_delete=models.CASCADE,null=True)
    cantidad = models.IntegerField(default=1)
    fkProducto =models.ForeignKey(Producto, on_delete=models.CASCADE,null=True)
    subtotal = models.FloatField(null=True,default=0)
    cebolla = models.IntegerField(default=0,null=True)
    aguacate = models.IntegerField(default=0, null=True)
    fkProducto = models.ForeignKey(Producto, on_delete=models.CASCADE,null=True)
    cebollaBase = models.IntegerField(default=0,null=True)
    def setFkPedido(self,valor):
        self.fkPedido=valor
    def setfkProdcto(self,valor):
        self.fkProducto=valor
    def setCantidad(self,valor):
        self.cantidad=valor
    def setCebolla(self,valor):
        self.cebolla=valor
    def setSubtotal(self):
        self.subtotal=float(self.cantidad*self.fkProducto.precio)
    def getSubtotal(self):
        return self.subtotal
    def getCategoria(self):
        return self.fkProducto.fkCategoriaProducto.id
    def setAguacate(self, valor):
        self.aguacate=valor
    def sumarExtras(self, valor):
        self.subtotal=self.subtotal+valor