from django.contrib import admin

# Register your models here.
# Insumo, CategoriaIncidencia, Mesa
# CategoriaProducto, Producto, ProductoInsumo
# Cuenta,Pedido, LineaDePedido,ProductoLinea

from apps.cajaCuenta.models import *
from apps.cajaAdmin.models import *

admin.site.register(Insumo)
admin.site.register(Mesa)
admin.site.register(CategoriaProducto)
admin.site.register(Producto)
admin.site.register(Transaccion)
admin.site.register(Cuenta)
admin.site.register(Pedido)
admin.site.register(LineaDePedido)
admin.site.register(Cupon)
admin.site.register(Mes)
admin.site.register(Receta)
admin.site.register(LineaDeReceta)
admin.site.register(Existencia)
