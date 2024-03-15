from django.shortcuts import render, redirect
from apps.cajaCuenta.models import Mesa
from django.contrib.auth.decorators import login_required
from apps.cajaCuenta.models import *
from apps.cajaAdmin.models import *
from datetime import datetime
# Create your views here.
@login_required
def cambiarEstadoMesa(request,idMesa):
	mesa = Mesa.objects.get(id=idMesa)
	if mesa.disponible == True:
		mesa.disponible = False
	else:
		mesa.disponible = True
	mesa.save()
	return redirect('supervisor:verEstadoSupervisor')

@login_required
def verEstadoSupervisor(request):
	mesa = Mesa.objects.order_by('id')
	return render(request, 'supervisor/verEstadoSupervisor.html',{'mesas': mesa})
@login_required
def indexSupervisor(request):
    now = datetime.now()
    transaccion = Transaccion.objects.all()
    producto = Producto.objects.all()
    mes = Mes.objects.all().order_by('id')
    cuenta = Cuenta.objects.all().filter(cancelado=False, )
    pedido = Pedido.objects.all().filter(modificado=False)
    linea = LineaDePedido.objects.all()
    contexto = {'meses': mes, 'cuentas': cuenta, 'pedidos': pedido, 'lineas': linea, 'transacciones': transaccion, 'dia': now, 'productos': producto}
    return render(request,'supervisor/indexSupervisor.html',contexto)