from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from apps.cajaCuenta.forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import ( CreateView,UpdateView, DeleteView)
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from apps.cajaAdmin.models import *
# Create your views here.


@login_required
def estadorestaurante(request):
	mesa = Mesa.objects.order_by('id')
	'''cuenta = Cuenta.objects.filter(archivado=False, cancelado=False)
	pedid=[]
	for cuent in cuenta:
		pedidos=Pedido.objects.order_by('fkCuenta').filter(cancelado=False,fkCuenta=cuent.id)
		for pedido in pedidos:
			pedid.append(pedido)
	contexto = {'mesas':mesa,'cuentas':cuenta,'pedidos':pedid}
	return render(request, 'caja/estadoRestaurante.html',contexto)'''
	return render(request, 'caja/estadoRestaurante.html',{'mesas': mesa})

#lineas de pedido
def agregarLinea(request,cuenta, idPedido,producto):
	if request.method=='POST':
		form=formulario(request.POST)
		if form.is_valid():
			lineaped=LineaDePedido()
			pro = Producto.objects.get(id=producto)
			ped = Pedido.objects.get(id=idPedido)
			if pro.fkCategoriaProducto.cocinaNormal == True:
				ped.tyh = True
			elif pro.fkCategoriaProducto.comidaMexicana == True:
				ped.mex = True
			lineaped.setfkProdcto(pro)
			lineaped.setFkPedido(Pedido.objects.get(id=idPedido))
			ped.setDisplay()
			form_data=form.cleaned_data
			extra = 0
			if form_data.get("cebollaBase"==None):
				lineaped.cebollaBase=0
			else:
				lineaped.cebollaBase=form_data.get("cebollaBase")
			if form_data.get("cantidad")==None:
				lineaped.setCantidad(1)
			else:
				lineaped.setCantidad(form_data.get("cantidad"))
			#asignacion de los extras
			#revision de la cebolla
			if form_data.get("cebolla")==None:
				lineaped.setCebolla(0)
			else:
				lineaped.setCebolla(form_data.get("cebolla"))
				extra=extra + float (  0.25 * int(form_data.get("cebolla")))

			#revision del aguacate
			if form_data.get("aguacate")==None:
				lineaped.setAguacate(0)
			else:
				lineaped.setAguacate(form_data.get("aguacate"))
				extra=extra +  float  (0.25 * int(form_data.get("aguacate")))
			lineaped.setSubtotal()
			lineaped.sumarExtras(extra)
			lineaped.save()
			cuent=Cuenta.objects.get(id=cuenta)
			cuent.setTotal(float(lineaped.getSubtotal()))
			ped.subtotal=ped.subtotal + float(lineaped.getSubtotal())
			ped.save()
			cuent.save()
			urlss='/caja/seguimientoPedido/'+str(idPedido)
			return HttpResponseRedirect(urlss)
	else:
		pedido=Pedido.objects.get(id=idPedido)
		cuenta=pedido.fkCuenta
		prod=Producto.objects.get(id=producto)
		form=formulario()
		contexto={'pedido':pedido,'cuenta':cuenta,'prod':prod,'form':form}
	return render(request,'caja/add.html',contexto)

def agregarLinea2(request,cuenta, idPedido,producto):
	if request.method=='POST':
		form=formulario(request.POST)
		if form.is_valid():
			lineaped=LineaDePedido()
			cuent=Cuenta.objects.get(id=cuenta)
			pro = Producto.objects.get(id=producto)
			ped = Pedido.objects.get(id=idPedido)
			if pro.fkCategoriaProducto.cocinaNormal == True:
				ped.tyh = True
			elif pro.fkCategoriaProducto.comidaMexicana == True:
				ped.mex = True
			conteoLineas=LineaDePedido.objects.filter(fkPedido=idPedido,cancelado=False).count()
			conteoPedidos=Pedido.objects.filter(fkCuenta=cuenta)			
			lineaped.setfkProdcto(pro)
			lineaped.setFkPedido(ped)
			ped.setDisplay()
			form_data=form.cleaned_data
			extra = 0
			if form_data.get("cebollaBase"==None):
				lineaped.cebollaBase=0
			else:
				lineaped.cebollaBase=form_data.get("cebollaBase")
			if form_data.get("cantidad")==None:
				lineaped.setCantidad(1)
			else:
				lineaped.setCantidad(form_data.get("cantidad"))
			#asignacion de los extras
			#revision de la cebolla
			if form_data.get("cebolla")==None:
				lineaped.setCebolla(0)
			else:
				lineaped.setCebolla(form_data.get("cebolla"))
				extra=extra + float (  0.25 * int(form_data.get("cebolla")))
			#revision del aguacate
			if form_data.get("aguacate")==None:
				lineaped.setAguacate(0)
			else:
				lineaped.setAguacate(form_data.get("aguacate"))
				extra=extra +  float  (0.25 * int(form_data.get("aguacate")))
			lineaped.setSubtotal()
			lineaped.sumarExtras(extra)
			lineaped.save()
			cuent.setTotal(float(lineaped.getSubtotal()))
			ped=Pedido.objects.get(id=idPedido)
			ped.subtotal=ped.subtotal + float(lineaped.getSubtotal())
			ped.modificado=True
			ped.save()
			cuent.save()
			return redirect ('/caja/editar/'+ str(cuent.id))
	else:
		pedido=Pedido.objects.get(id=idPedido)
		cuenta=pedido.fkCuenta
		prod=Producto.objects.get(id=producto)
		form=formulario()
		contexto={'pedido':pedido,'cuenta':cuenta,'prod':prod,'form':form}
	return render(request,'caja/add2.html',contexto)

def cancelarLinea(request,pedido):
	urlss='/caja/seguimientoPedido/'+pedido
	return HttpResponseRedirect(urlss)


def borrarLinea(request,idLinea,idPedido):
	linea = LineaDePedido.objects.get(id=idLinea)
	pedido = Pedido.objects.get(id=linea.fkPedido.id)
	cuenta = Cuenta.objects.get(id=pedido.fkCuenta.id)
	pedido.subtotal = pedido.subtotal - linea.getSubtotal()
	cuenta.total = cuenta.total - linea.getSubtotal()
	lineasDelPedido=LineaDePedido.objects.filter(fkPedido=pedido.id,cancelado=False)
	val=0
	for lineaq in lineasDelPedido:
		if lineaq.fkProducto.fkCategoriaProducto == 1:
			val=val+1
	if val == 0 :
		pedido.tyh=False
	pedido.save()
	cuenta.save()
	linea.delete()
	urlss='/caja/seguimientoPedido/'+idPedido
	return HttpResponseRedirect(urlss)

#final lineas de pedido

#ventas

def seguimientoPedido(request,pedido):
	pedid=Pedido.objects.get(id=pedido)
	cuenta=pedid.fkCuenta
	categoria = CategoriaProducto.objects.all()
	linea=LineaDePedido.objects.filter(fkPedido=pedid)
	conteo=LineaDePedido.objects.filter(fkPedido=pedid).count()
	productos=[]
	for cat in categoria:
		diccionario={}
		pros = Producto.objects.filter(fkCategoriaProducto=cat.id).order_by('id','nombreProd')
		if bool(pros) :
			diccionario['categoria']=cat
			diccionario['productos']= pros
			productos.append(diccionario)
	contexto = {'lineas':linea,'pedido':pedid,'cuenta':cuenta,'productos':productos,'valor':conteo,'primero':productos[0]}
	return render(request,'caja/generarPedidos.html',contexto)



# inicializa la venta o no
def iniciarVenta(request):
	if request.method=='POST':
		form = guardarVenta(request.POST)
		if form.is_valid():
			form_data=form.cleaned_data
			cuenta = Cuenta()
			cuenta.save()
			if form_data.get("check")==True:
				cuenta.setCliente(form_data.get("nombre"))
				cuenta.naturaleza=True
				cuenta.save()
				urlss='/caja/venta/'+str(cuenta.id)
				return HttpResponseRedirect(urlss)
			else:
				if form_data.get("check2")==True:
					cuenta.setCliente(form_data.get("nombre"))
					cuenta.setDelivery(True)
					cuenta.setDireccion(form_data.get("direccion"))
					cuenta.telefono=form_data.get('numero')
					cuenta.save()
					urlss='/caja/venta/'+str(cuenta.id)
					return HttpResponseRedirect(urlss)
				else:
					if form_data.get("valMesa")==1:
						mesirijilla=str(form_data.get("mesa").get())
						cuenta.setMesa(Mesa.objects.get(id=mesirijilla))
						cuenta.setCliente('')
						mesa=Mesa.objects.get(id=mesirijilla)
						mesa.setDisponible(False)
						mesa.save()
						cuenta.save()
						urlss='/caja/venta/'+str(cuenta.id)
						return HttpResponseRedirect(urlss)
	else:
		form=guardarVenta()
		conteo=Mesa.objects.filter(disponible=True).count()
		contexto={'form':form,'valor':conteo}
	return render(request,'caja/inicializar.html',contexto)

def crearReincidente(request,cuenta):#para los pedidos reincidentes
	cuent=Cuenta.objects.get(id=cuenta)
	cuent.setAunEnCocina(True)
	return render(request,'caja/seleccion.html',{'cuenta':cuent})

def crearVentaReincidenteLlevar(request,cuenta):
	cuentirijilla=Cuenta.objects.get(id=cuenta)
	cuentirijilla.setAunEnCocina(True)
	cuentirijilla.save()
	pedido = Pedido()
	pedido.setFK(cuentirijilla)
	pedido.setParaLlevar(True)
	pedido.save()
	categoria = CategoriaProducto.objects.all()
	valor=0
	productos=[]
	for cat in categoria:
		diccionario={}
		pros = Producto.objects.filter(fkCategoriaProducto=cat.id).order_by('id','nombreProd')
		if bool(pros) :
			diccionario['categoria']=cat
			diccionario['productos']= pros
			productos.append(diccionario)
	contexto = {'pedido':pedido,'cuenta':cuentirijilla,'productos':productos,'categorias':categoria,'valor':valor,'primero':productos[0]}
	return render(request,'caja/generarPedidos.html',contexto)

def crearVentaReincidenteAqui(request,cuenta):
	cuentirijilla=Cuenta.objects.get(id=cuenta)
	cuentirijilla.setAunEnCocina(True)
	cuentirijilla.save()
	pedido = Pedido()
	pedido.setFK(cuentirijilla)
	pedido.save()
	categoria = CategoriaProducto.objects.all()
	valor=0
	productos=[]
	for cat in categoria:
		diccionario={}
		pros = Producto.objects.filter(fkCategoriaProducto=cat.id).order_by('id','nombreProd')
		if bool(pros) :
			diccionario['categoria']=cat
			diccionario['productos']= pros
			productos.append(diccionario)
	contexto = {'pedido':pedido,'cuenta':cuentirijilla,'productos':productos,'categorias':categoria,'valor':valor,'primero':productos[0]}
	return render(request,'caja/generarPedidos.html',contexto)


def crearVenta(request,cuenta):#creando nuevo pedido
	cuentirijilla=Cuenta.objects.get(id=cuenta)
	cuentirijilla.setAunEnCocina(True)
	cuentirijilla.save()
	pedido = Pedido()
	pedido.setFK(cuentirijilla)
	if cuentirijilla.fkMesa==None:
		pedido.setParaLlevar(True)
	pedido.save()
	categoria = CategoriaProducto.objects.all()
	valor=0
	productos=[]
	for cat in categoria:
		diccionario={}
		pros = Producto.objects.filter(fkCategoriaProducto=cat.id).order_by('id','nombreProd')
		if bool(pros) :
			diccionario['categoria']=cat
			diccionario['productos']= pros
			productos.append(diccionario)
	contexto = {'pedido':pedido,'cuenta':cuentirijilla,'productos':productos,'categorias':categoria,'valor':valor,'primero':productos[0]}
	return render(request,'caja/generarPedidos.html',contexto)

def crearVenta2(request,cuenta,pedido):#creando nuevo pedido
	cuentirijilla=Cuenta.objects.get(id=cuenta)
	pedido=Pedido.objects.get(id=pedido)
	categoria = CategoriaProducto.objects.all()
	productos=[]
	for cat in categoria:
		diccionario={}
		pros = Producto.objects.filter(fkCategoriaProducto=cat.id).order_by('id','nombreProd')
		if bool(pros) :
			diccionario['categoria']=cat
			diccionario['productos']= pros
			productos.append(diccionario)
	contexto = {'pedido':pedido,'cuenta':cuentirijilla,'productos':productos,'categorias':categoria,'primero':productos[0]}
	return render(request,'caja/generarPedidos2.html',contexto)

def terminarVenta(request,pedido):
	if request.method=='POST':
		form = comentario(request.POST)
		if form.is_valid():
			form_data=form.cleaned_data
			pedido=Pedido.objects.get(id=pedido)
			cuenta=Cuenta.objects.get(id=pedido.fkCuenta.id)
			if cuenta.fkMesero==None:
				cuenta.fkMesero=str(form_data.get("usuario").get())
			cuenta.visible=True
			cuenta.final=False
			cuenta.impreso=False
			cuenta.save()
			pedido.setComentario(form_data.get("comentario"))
			pedido.setPrioridad(form_data.get("prioridad"))
			pedido.fkMesero=str(form_data.get("usuario").get())
			pedido.setCocina(True)
			pedido.exito=True
			pedido.save()
			if request.user.is_authenticated:
				return redirect('caja:indexcajero')
			else:
				return redirect('caja:indexmes')
	form=comentario()
	pedido=Pedido.objects.get(id=pedido)
	return render(request,'caja/confirmar.html',{'form':form,'pedido':pedido})

def impresion(request,cuenta):
			cuent=Cuenta.objects.get(id=cuenta)
			cuent.setImpreso(True)
			cuent.save()
			if request.user.is_authenticated:
				return redirect('/caja/detalleventa/' + cuenta )
			else:
				return redirect('caja:indexmes')

def impresion2(request):
			return redirect('gerente:generador')

def cancelarVenta(request, cuent,pedid):
	pedidos=Pedido.objects.filter(fkCuenta=cuent,exito=True).count()
	pedido=Pedido.objects.get(id=pedid)
	if pedidos == 0:	
		LineaDePedido.objects.filter(fkPedido=pedid).delete()
		cuenta=Cuenta.objects.get(id=cuent)
		if pedido.paraLlevar == False:
			mesa=Mesa.objects.get(id=cuenta.fkMesa.id)
			mesa.setDisponible(True)
			mesa.save()
		pedido.delete()
		cuenta.delete()
		if request.user.is_authenticated:
			return redirect('caja:indexcajero')
		else:
			return redirect('caja:indexmes')
	else:
		pedido.delete()
		LineaDePedido.objects.filter(fkPedido=pedid).delete()
		if request.user.is_authenticated:
			return redirect('caja:indexcajero')
		else:
			return redirect('caja:indexmes')
##final venta

##index ambos roles
def indexmes(request):
	cuenta = Cuenta.objects.filter(archivado=False).order_by('fkMesa','fechaCuenta','horaCuenta')
	pedidos = []
	for cuen in cuenta:
		pedido = Pedido.objects.filter(fkCuenta=cuen.id,exito=True,cancelado=False)
		factura= {}
		factura['cuenta']= cuen
		factura['pedido']= pedido
		pedidos.append(factura)
	contexto = {'pedidos':pedidos}
	return render(request,'mesero/inicio.html',contexto)

@login_required
def indexCa(request):
	cuenta = Cuenta.objects.filter(archivado=False).order_by('fkMesa','fechaCuenta','horaCuenta')
	pedidos = []
	for cuen in cuenta:
		pedido = Pedido.objects.filter(fkCuenta=cuen.id,exito=True,cancelado=False)
		factura= {}
		factura['cuenta']= cuen
		factura['pedido']= pedido
		pedidos.append(factura)
	contexto = {'cuentas':pedidos}
	return render(request,'caja/cajeroIndex.html', contexto)
##final index
@login_required
def detalleVenta(request, idCuenta):
	cuenta = Cuenta.objects.get(id=idCuenta)
	pedido = Pedido.objects.filter(fkCuenta=idCuenta,cancelado=False)
	pedidosC= Pedido.objects.filter(fkCuenta=idCuenta,cobrado=True,cancelado=False)
	pedidoCocina = Pedido.objects.filter(fkCuenta=idCuenta,enCocina=False,cancelado=False)
	pedidosS = Pedido.objects.filter(fkCuenta=idCuenta,enCocina=True,cancelado=False)
	control = False
	if pedido == pedidosS:
		control = True
	servido = False
	if ( pedido.count() - pedidoCocina.count() ) == 0 :
		print(pedido.count() - pedidosC.count() )
		servido = True
	total=cuenta.total
	for ped in pedidosC:
		total = total - ped.subtotal
	linea=[]
	for pedi in pedido:
		lineas=LineaDePedido.objects.filter(fkPedido=pedi.id,cancelado=False)
		for lin in lineas:
			linea.append(lin)
	contexto = {'mesas': mesa, 'cuentas': cuenta, 'pedidos': pedido, 'lineas': linea,'total':total,'servido':servido,'control':control}
	return render(request, 'caja/verDetalleVenta.html', contexto)

def lineaped(request, idPedido):
	cuenta = Cuenta.objects.filter(id=idPedido)
	pedido = Pedido.objects.get(id=idPedido)
	linea = LineaDePedido.objects.filter(cancelado=False,fkPedido=idPedido)
	contexto = {'cuentas': cuenta, 'pedidos': pedido, 'lineas': linea}
	return render(request, 'caja/detapedid.html', contexto)

def lineaped2(request, idPedido):
	cuenta = Cuenta.objects.filter(id=idPedido)
	pedido = Pedido.objects.get(id=idPedido)
	linea = LineaDePedido.objects.filter(fkPedido=idPedido)
	contexto = { 'cuentas': cuenta, 'pedidos': pedido, 'lineas': linea,}
	return render(request, 'caja/detapedid2.html', contexto)

def cobrar(request,idCuenta):
	cuenta = Cuenta.objects.get(id=idCuenta)
	pedido = Pedido.objects.filter(fkCuenta=idCuenta,cancelado=False)
	total=cuenta.total
	pedidosC= Pedido.objects.filter(fkCuenta=idCuenta,cobrado=True)
	#cuento la cantidad de pedidos y luego la cantidad de pedidos servidos
	pedidosS=Pedido.objects.filter(fkCuenta=idCuenta,enCocina=False).count()
	pedidos=Pedido.objects.filter(fkCuenta=idCuenta).count()
	control = False
	if pedidos == pedidosS:
		control = True
	for ped in pedidosC:
		total = total - ped.subtotal
	linea=[]
	for pedi in pedido:
		lineas=LineaDePedido.objects.filter(fkPedido=pedi.id,cancelado=False)
		for lin in lineas:
			linea.append(lin)
	contexto = { 'cuentas': cuenta, 'pedidos': pedido, 'lineas': linea,'total':total,'control':control}
	return render(request, 'mesero/cobro.html', contexto)

def reasignarMesa(request, idCuenta):
	if request.method == 'POST':
		formulario = formMesas(request.POST)
		if formulario.is_valid() == True:
			form_data = formulario.cleaned_data
			cuenta = Cuenta.objects.get(id=idCuenta)
			mesa = cuenta.fkMesa
			mesa.disponible = True
			mesa.save()
			mesirijilla = str(form_data.get("mesa").get())
			mesita = Mesa.objects.get(id=mesirijilla)
			cuenta.setMesa(mesita)
			mesita.setDisponible(False)
			mesita.save()
			cuenta.save()
			return redirect('/caja/cobrar/'+str(idCuenta))
		else:
			return redirect('/caja/cobrar/' + str(idCuenta))
	else:
		form = formMesas()
		contexto = {'form': form, 'idCuenta': idCuenta}
		return render(request, 'mesero/reasignarMesa.html', contexto)

@login_required
def efectuarCobro(request,idCuenta):
	cuenta=Cuenta.objects.get(id=idCuenta)
	cuenta.setFinal(True)
	cuenta.save()
	#cuenta.setArchivado(True)
	pedidos=Pedido.objects.filter(fkCuenta=idCuenta)
	for ped in pedidos:
		ped.cobrado = True
		ped.save()
	pedidosS=Pedido.objects.filter(fkCuenta=idCuenta,enCocina=False ).count()
	control = False
	if pedidos.count() == pedidosS:
		control = True
	if control == True:
		if(cuenta.fkMesa!=None):
			mesa=Mesa.objects.get(id=cuenta.fkMesa.id)
			mesa.setDisponible(True)
			mesa.save()
		cuenta.archivado=True
		cuenta.save()
	return redirect('caja:indexcajero')

def cocina(request):
	pedido = Pedido.objects.filter(cancelado=False,enCocina=True,display=True,tyh=True).order_by('horaPedido')
	#lista de pedidos filtrados
	diccionarioPedidos=[]
	for ped in pedido:
		diccionarioLineasPedido={}
		diccionarioLineasPedido['pedido']=ped
		diccionarioLineasPedido['lineas']=LineaDePedido.objects.filter(cancelado=False,fkPedido=ped.id)
		diccionarioPedidos.append(diccionarioLineasPedido)
	contexto = {'pedidos':diccionarioPedidos}
	return render(request,'caja/cocina.html',contexto)
@login_required
def validar(request,idCuenta):
	if request.method == 'POST':		
		cuenta=Cuenta.objects.get(id=idCuenta)
		cuenta.fkCajero=request.user.username
		cuenta.save()
		return redirect('caja:efectuarCobro',idCuenta)
	else:
		return render (request,'caja/validar.html',{'idCuenta':idCuenta})

def cambiarEstado(request,idPedido,idCuenta):
	pedido=Pedido.objects.get(id=idPedido)
	cuent=Cuenta.objects.get(id=idCuenta)
	if pedido.getCocina() == True:
		pedido.setCocina(False)
		cuent.setAunEnCocina(False)
		lineas=LineaDePedido.objects.filter(fkPedido=pedido.id)#lineas de pedido
		for linea in lineas:
			producto = linea.fkProducto
			cantidad = linea.cantidad
			lineasReceta = LineaDeReceta.objects.filter(fkReceta=producto.receta.id)#lineas de receta del producto
			for lineaReceta in lineasReceta:
				existencia = Existencia.objects.get(fkInsumo=lineaReceta.fkInsumo)
				existencia.disminuir( cantidad * lineaReceta.cantidad )
				existencia.save()
	else:
		pedido.setCocina(True)
		cuent.setAunEnCocina(True)
		lineas=LineaDePedido.objects.filter(fkPedido=pedido.id)#lineas de pedido
	pedido.save()
	cuent.save()
	return render(request,'caja/cambiarEstado.html',{'pedido':pedido})
@login_required
def descuento(request,cuenta):
	formulario=ticketIngresar()
	contexto={'form':formulario,'cuenta':cuenta}
	if request.method=='POST':
		formulario=ticketIngresar(request.POST)
		if formulario.is_valid()==True:
			form_data=formulario.cleaned_data
			cod=form_data.get('valor')
			cuent=Cuenta.objects.get(id=cuenta)
			try:
				cupon=Cupon.objects.get(codigo=cod)
				if cupon.usado == False:
					cuent.descuento(cupon.porcentaje)
					cuent.save()
					cupon.delete()
			except :
				print("hola")
			return redirect('caja:detallevent',cuenta)
	return render(request,'caja/cupones.html',contexto)

def editar(request,cuenta):
	cuent=Cuenta.objects.get(id=cuenta)
	pedidos=Pedido.objects.filter(fkCuenta=cuent.id)
	lineas=[]
	for ped in pedidos:
		lineas.extend(list(LineaDePedido.objects.filter(fkPedido=ped.id)))
	contexto={'cuenta':cuent,'pedidos':pedidos,'lineas':lineas}
	return render(request,'mesero/editarPedido.html',contexto)

def eliminarCuenta(request,cuenta):
	formulario=comentarioObligatorio()
	contexto={'form':formulario,'cuenta':cuenta}
	if request.method=='POST':
		formulario=comentarioObligatorio(request.POST)
		if formulario.is_valid():
			form_data=formulario.cleaned_data
			cuent=Cuenta.objects.get(id=cuenta)
			pedidos=Pedido.objects.filter(fkCuenta=cuent.id)
			cuent.fkMesero=str(form_data.get("usuario").get())
			cuent.comentario=form_data.get("comentario")
			cuent.modificado=True
			cuent.archivado=True
			cuent.cancelado=True
			cuent.aunEnCocina=False
			cuent.save()
			for ped in pedidos:
				ped.enCocina=False
				ped.save()
			if cuent.fkMesa != None:
				mesa=Mesa.objects.get(id=cuent.fkMesa.id)
				mesa.disponible=True
				mesa.save()
			return redirect ('caja:indexmes')
	return render(request,'mesero/eliminarCuenta.html',contexto)

def eliminarPedido(request,pedido):
	formulario=comentarioObligatorio()
	contexto={'form':formulario,'pedido':pedido}
	if request.method=='POST':
		formulario=comentarioObligatorio(request.POST)
		if formulario.is_valid():
			form_data=formulario.cleaned_data
			pedid=Pedido.objects.get(id=pedido)
			cuent=Cuenta.objects.get(id=pedid.fkCuenta.id)
			pedidos=Pedido.objects.filter(fkCuenta=cuent.id,cancelado=False)
			conteo=pedidos.count()
			cuent.modificado=True
			cuent.save()
			lineas=LineaDePedido.objects.filter(id=pedid.id)
			if conteo == 1:
				cuent.fkMesero=str(form_data.get("usuario").get())
				if pedid.comentariomod != None:
					pedid.comentariomod=pedid.comentariomod+"/n"+form_data.get("comentario")
				else:
					pedid.comentariomod=form_data.get("comentario")
				cuent.aunEnCocina=False
				cuent.modificado=True
				pedid.cancelado=True
				pedid.exito=False
				pedid.enCocina=False
				pedid.fkMesero=str(form_data.get("usuario").get())
				pedid.comentariomod=pedid.comentariomod+"/n"+form_data.get("comentario")
				pedid.save()
				cuent.save()
				return redirect ('/caja/editar/'+ str(cuent.id))
			else:
				pedid.comentariomod=form_data.get("comentario")
				pedid.fkMesero=str(form_data.get("usuario").get())
				pedid.modificado=True
				pedid.enCocina=False
				cuent.total=cuent.total-pedid.subtotal
				pedid.cancelado=True
				cuent.modificado=True
				cuent.save()
				pedid.save()
				return redirect ('/caja/editar/'+str(cuent.id))
	return render(request,'mesero/eliminarPedido.html',contexto)

def eliminarPedido2(request,pedido):
	formulario=comentarioObligatorio()
	contexto={'form':formulario,'pedido':pedido}
	if request.method=='POST':
		formulario=comentarioObligatorio(request.POST)
		if formulario.is_valid():
			form_data=formulario.cleaned_data
			pedid=Pedido.objects.get(id=pedido)
			cuent=Cuenta.objects.get(id=pedid.fkCuenta.id)
			pedidos=Pedido.objects.filter(fkCuenta=cuent.id,cancelado=False)
			conteo=pedidos.count()
			lineas=LineaDePedido.objects.filter(fkPedido=pedid.id)
			cuent.modificado=True
			cuent.save()
			for linea in lineas:
					producto=Producto.objects.get(id=linea.fkProducto.id)
					receta=Receta.objects.get(id=producto.receta.id)
					lineasDeReceta=LineaDeReceta.objects.filter(fkReceta=receta.id)
					for lineaDeReceta in lineasDeReceta:
						#teniendo en cuenta que las categorías de comida son 1 hamburguesas/tortas y 2 la comida mexicana
						if producto.fkCategoriaProducto.id != 2 and  producto.fkCategoriaProducto.id != 1:
							insumo=Insumo.objects.get(id=lineaDeReceta.fkInsumo.id)
							existencia=Existencia.objects.get(fkInsumo=insumo.id)
							existencia.aumentar(linea.cantidad * lineaDeReceta.cantidad)
							existencia.save()
			if conteo == 1:
				cuent.fkMesero=str(form_data.get("usuario").get())
				if pedid.comentariomod != None:
					pedid.comentariomod=pedid.comentariomod+"/n"+form_data.get("comentario")
				else:
					pedid.comentariomod=form_data.get("comentario")
				cuent.archivado=True
				cuent.aunEnCocina=False
				pedid.cancelado=True
				cuent.save()
				pedid.enCocina=False
				pedid.fkMesero=str(form_data.get("usuario").get())
				pedid.comentariomod=pedid.comentariomod+"/n"+form_data.get("comentario")
				pedid.save()
				if cuent.fkMesa != None:
					mesa=Mesa.objects.get(id=cuent.fkMesa.id)
					mesa.disponible=True
					mesa.save()
				cuent.save()
				return redirect ('/caja/editar/'+ str(cuent.id))
			else:
				pedid.comentariomod=form_data.get("comentario")
				pedid.fkMesero=str(form_data.get("usuario").get())
				pedid.modificado=True
				pedid.enCocina=False
				cuent.total=cuent.total-pedid.subtotal
				pedid.cancelado=True
				cuent.save()
				pedid.save()
				return redirect ('/caja/editar/'+str(cuent.id))
	return render(request,'mesero/eliminarPedido2.html',contexto)

def eliminarLinea(request,linea):
	if request.method=='POST':
		formulario=comentarioObligatorio(request.POST)
		if formulario.is_valid():
			form_data=formulario.cleaned_data
			lin=LineaDePedido.objects.get(id=linea )
			lin.cancelado =True
			lin.comentarioMod=form_data.get("comentario")
			lin.save()
			pedid=Pedido.objects.get(id=lin.fkPedido.id)
			cuent=Cuenta.objects.get(id=pedid.fkCuenta.id)			
			pedidos=Pedido.objects.filter(fkCuenta=cuent.id,cancelado=False).count()
			lineas=LineaDePedido.objects.filter(fkPedido=pedid.id, cancelado=False).count()
			pedid.fkMesero=str(form_data.get("usuario").get())
			if pedid.comentariomod != None:
					pedid.comentariomod=pedid.comentariomod+"/n"+form_data.get("comentario")
			else:
				pedid.comentariomod=form_data.get("comentario")
			if pedid.enCocina == False:
				producto = Producto.objects.get(id=lin.fkProducto.id)
				receta=Receta.objects.get(id=producto.receta.id)
				lineasDeReceta=LineaDeReceta.objects.filter(fkReceta=receta.id)
				for lineaDeReceta in lineasDeReceta:
					#teniendo en cuenta que las categorías de comida son 1 hamburguesas/tortas y 2 la comida mexicana
					if producto.fkCategoriaProducto.id != 2 and  producto.fkCategoriaProducto.id != 1:
						insumo=Insumo.objects.get(id=lineaDeReceta.fkInsumo.id)
						existencia=Existencia.objects.get(fkInsumo=insumo.id)
						existencia.aumentar(lin.cantidad * lineaDeReceta.cantidad)
						existencia.save()
			cuent.total=cuent.total-lin.subtotal
			cuent.modificado=True
			if pedidos == 1:
				if lineas == 0:
					cuent.aunEnCocina=False
					pedid.modificado=True
					pedid.tyh=False
					cuent.fkMesero=str(form_data.get("usuario").get())
					if cuent.comentario != None:
						cuent.comentario=pedid.comentariomod+"/n"+form_data.get("comentario")
					else:
						cuent.comentario=form_data.get("comentario")
				else:
					if cuent.comentario != None:
						cuent.comentario=pedid.comentariomod+"/n"+form_data.get("comentario")
					else:
						cuent.comentario=form_data.get("comentario")
					lineasDelPedido=LineaDePedido.objects.filter(fkPedido=pedid.id,cancelado=False)
					print(lineasDelPedido.count())
					val=0
					for linea in lineasDelPedido:
						if linea.fkProducto.fkCategoriaProducto.id == 1:
							val=val+1
					if val == 0 :
						pedid.tyh=False
			else:
				if lineas == 0:
					pedid.modificado=True
					pedid.tyh=False
					if cuent.comentario != None:
						cuent.comentario=pedid.comentariomod+"/n"+form_data.get("comentario")
					else:
						cuent.comentario=form_data.get("comentario")
				else:
					if cuent.comentario != None:
						cuent.comentario=pedid.comentariomod+"/n"+form_data.get("comentario")
					else:
						cuent.comentario=form_data.get("comentario")
					lineasDelPedido=LineaDePedido.objects.filter(fkPedido=pedid.id,cancelado=False)
					val=0
					for linea in lineasDelPedido:
						if linea.fkProducto.fkCategoriaProducto.id == 1:
							val=val+1
					if val == 0 :
						pedid.tyh=False
			pedid.save()
			cuent.save()
			return redirect ('/caja/editar/'+ str(cuent.id))
	else:
		formulario=comentarioObligatorio()
		contexto={'form':formulario,'linea':linea}
		return render(request,'mesero/eliminarLinea.html',contexto)

def editarLinea(request,linea):
	lin=LineaDePedido.objects.get(id=linea)
	pedido=Pedido.objects.get(id=lin.fkPedido.id)
	cuent=Cuenta.objects.get(id=pedido.fkCuenta.id)
	if request.method=='POST':
		form=formulario(request.POST)
		if form.is_valid():
			pedido=Pedido.objects.get(id=lin.fkPedido.id)
			cuent=Cuenta.objects.get(id=pedido.fkCuenta.id)
			cuent.total=cuent.total - lin.subtotal
			pedido.subtotal=pedido.subtotal - lin.getSubtotal()	
			form_data=form.cleaned_data
			linCant=lin.cantidad
			linExtras=0.25 * (lin.cebolla + lin.aguacate)
			#setting cebolla/cantidad
			extra = 0
			if form_data.get("cebollaBase") == None:
				lin.cebollaBase=0
			else:
				lin.cebollaBase=form_data.get("cebollaBase")
			if form_data.get("cantidad")==None:
				lin.setCantidad(1)
			else:
				lin.setCantidad(form_data.get("cantidad"))
			#asignacion de los extras
			#revision de la cebolla
			if form_data.get("cebolla")==None:
				lin.setCebolla(0)
			else:
				lin.setCebolla(form_data.get("cebolla"))
				extra=extra + float (  0.25 * int(form_data.get("cebolla")))
			#revision del aguacate
			if form_data.get("aguacate")==None:
				lin.setAguacate(0)
			else:
				lin.setAguacate(form_data.get("aguacate"))
				extra=extra +  float  (0.25 * int(form_data.get("aguacate")))
			#
			lin.setSubtotal()			
			lin.sumarExtras(extra)
			cuent.setTotal(float(lin.getSubtotal()))
			pedido.subtotal=pedido.subtotal + float(lin.getSubtotal())	
			lin.modificado=True
			pedido.modificado=True
			cuent.modificado=True
			lin.comentarioMod="La linea pasó de tener una cantidad de: "+ str(linCant) +" a tener: " +str(lin.cantidad) + " y un cobro extra de: " + str(linExtras) + " a un cobro de: "+str(extra)
			lin.save()	
			pedido.save()
			cuent.save()
			return redirect ('/caja/editar/'+ str(cuent.id))
	initialData={
		'cantidad':lin.cantidad,
		'cebollaBase':lin.cebollaBase,
		'cebolla':lin.cebolla,
		'aguacate':lin.aguacate
	}
	formu=formulario2(initial=initialData)
	prod=Producto.objects.get(id=lin.fkProducto.id)
	contexto={'form':formu,'linea':lin,'prod':prod,'cuenta':cuent}
	return render(request,'mesero/editarLinea.html',contexto)

def archivar(request, idCuenta):
	cuenta = Cuenta.objects.get(id=idCuenta)
	cuenta.setArchivado(True)
	cuenta.save()
	if cuenta.fkMesa != None:
		mesa=Mesa.objects.get(id=cuenta.fkMesa.id)
		mesa.disponible=True
		mesa.save()
	return redirect("/caja/indexM/")


	