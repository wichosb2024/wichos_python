from __future__ import unicode_literals
from __future__ import absolute_import
from django.conf.urls import url
from apps.cajaCuenta.views import *
app_name='caja'
urlpatterns=[
url(r'^archivar/(?P<idCuenta>\w+)', archivar,name="archivar"),
url(r'^indexM/', indexmes,name="indexmes"),
url(r'^seguimientoPedido/(?P<pedido>\w+)', seguimientoPedido, name="seguimientoPedido"),
url(r'^estadorest/', estadorestaurante, name="estadores"),
url(r'^venta/(?P<cuenta>\w+)', crearVenta, name="venta"),
url(r'^venta2/(?P<cuenta>\w+)/(?P<pedido>\w+)', crearVenta2, name="venta2"),
url(r'^detalin/(?P<idPedido>\w+)', lineaped, name="lin"),
url(r'^detalin2/(?P<idPedido>\w+)', lineaped2, name="lin2"),
url(r'^cancelarLinea/(?P<pedido>\w+)',cancelarLinea,name="cancelarLinea"),
url(r'^cancelar/(?P<cuent>\w+)/(?P<pedid>\w+)/', cancelarVenta, name="cancelar"),
url(r'^indexcaja/', indexCa, name="indexcajero"),
url(r'^add/(?P<cuenta>\w+)/(?P<idPedido>\w+)/(?P<producto>\w+)', agregarLinea,name="add"),
url(r'^add2/(?P<cuenta>\w+)/(?P<idPedido>\w+)/(?P<producto>\w+)', agregarLinea2,name="add2"),
url(r'^detalleventa/(?P<idCuenta>\w+)', detalleVenta, name="detallevent"),
url(r'^reasignarMesa/(?P<idCuenta>\w+)', reasignarMesa, name="reasignarMesa"),
url(r'^eliminarLinea/(?P<idPedido>\w+)/(?P<idLinea>\w+)',borrarLinea,name="borrarLinea"),
url(r'^iniciarVenta/',iniciarVenta,name="iniciarVenta"),
url(r'^terminarVenta/(?P<pedido>\w+)', terminarVenta, name="terminarVenta"),
url(r'^impresion/(?P<cuenta>\w+)', impresion, name="impresion"),
url(r'^cobrar/(?P<idCuenta>\w+)', cobrar, name="cobrar"),
url(r'^efectuarCobro/(?P<idCuenta>\w+)', efectuarCobro, name="efectuarCobro"),
url(r'^cocin/', cocina, name="cocin"),
url(r'^validar/(?P<idCuenta>\w+)', validar, name="validar"),
url(r'^cambiarestado/(?P<idPedido>\w+)/(?P<idCuenta>\w+)/', cambiarEstado,name="cambiarestado"),
url(r'^rein/(?P<cuenta>\w+)/', crearReincidente,name="rein"),
url(r'^cvrl/(?P<cuenta>\w+)/', crearVentaReincidenteLlevar,name="cvrl"),
url(r'^cvra/(?P<cuenta>\w+)/', crearVentaReincidenteAqui,name="cvra"),
url(r'^descuento/(?P<cuenta>\w+)/', descuento,name="descuento"),
url(r'^editar/(?P<cuenta>\w+)', editar, name="editar"),
url(r'^eliminarCuenta/(?P<cuenta>\w+)', eliminarCuenta, name="eliminarCuenta"),
url(r'^eliminarPedido/(?P<pedido>\w+)', eliminarPedido, name="eliminarPedido"),
url(r'^eliminarPedido2/(?P<pedido>\w+)', eliminarPedido2, name="eliminarPedido2"),
url(r'^eliminarLinea/(?P<linea>\w+)', eliminarLinea, name="eliminarLinea"),
url(r'^editarLinea/(?P<linea>\w+)', editarLinea, name="editarLinea"),


]