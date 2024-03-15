from __future__ import unicode_literals
from __future__ import absolute_import
from django.conf.urls import url
from apps.cajaAdmin.views import *
from apps.cajaAdmin import views as core_views
from django.views.generic import TemplateView
app_name='gerente'
urlpatterns=[
url(r'^estadoresta/', estadorestaurant, name="estadorestaur"),
#url(r'^venta/', gestventa, name="venta"),
url(r'^prinadmin/', indexGerente, name="indexger"),
url(r'^verinv/', verinventario, name="verinve"),
url(r'^gestins/(?P<idInsumo>\w+)', gestinsumo, name="gestinsu"),
url(r'^gestprd/(?P<idProducto>\w+)', gestproduct, name="gestprd"),
url(r'^addins/', addinsumo, name="addinsu"),
url(r'^graftdin/', grafdinero, name="graftdine"),
url(r'^regist/', registros, name="registrs"),
url(r'^vervent/', verventas, name="verventa"),
url(r'^detcue/(?P<idCuenta>\w+)', detacue, name="detallecue"),
url(r'^agregarProduct/', agregarProducto, name="agregarProduct"),
url(r'^generador/', generarTickets, name="generador"),
url(r'^elimina1/(?P<cod>\w+)', elimina1, name="elimina1"),
url(r'^eliminato2/', eliminato2, name="eliminato2"),
url(r'^gestmes/(?P<idMes>\w+)', gestmes, name="gestmes"),
url(r'^dindiario/', prodDiarios, name="proddiarios"),
url(r'^proddiarios/', prodDiarios2, name="proddiarios2"),
url(r'^proddiariosdinero/', prodDiariosM, name="proddinero"),
url(r'^addeg/', addtransaccion, name="adde"),
url(r'^eliminarTr/(?P<idTransaccion>\w+)',eliminaT,name="eliminarTransaccion"),
url(r'^eliminarPrd/(?P<idProducto>\w+)',eliminaPrd,name="eliminarPrd"),
url(r'^meseros',meseros,name="meseros"),
url(r'^registroMeseros',core_views.signup,name="registroMesero"),
url(r'^cambiarContrasenia/(?P<idUsuario>\w+)',cambiarContrasenia,name="cambiarContrasenia"),
url(r'^eliminar_usuario',eliminar_usuario,name="eliminar_usuario"),
url(r'^categorias',categorias,name="categorias"),
url(r'^addCategoria',addCategoria,name="addCategoria"),
url(r'^eliminarCategoria',eliminarCategoria,name="eliminarCategoria"),
url(r'^editarCategoria//(?P<idCategoria>\w+)',editarCategoria,name="editarCategoria"),
url(r'^verprod/', product, name="prodc"),
]