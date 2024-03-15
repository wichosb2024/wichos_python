#path('caja/', include('apps.cajaCuenta.urls')),
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from apps.cajaCuenta.models import *
from .forms import *
from django.views.generic import *
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import *
from .models import *
from random import randrange, choice
from django.views.generic.edit import UpdateView
from datetime import date, datetime
from django.contrib.auth.models import User, Group
# Create your views here.
@login_required
def agregarProducto(request):
    if request.user.groups.filter(name='administrador').exists():
        if request.method == 'POST':
            form = productoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('gerente:prodc')
        else:
            form = productoForm()
        return render(request,'gerente/agregarProducto.html',{'form':form})
    else:
        return redirect ('ingreso:ingresar')

@login_required
def indexGerente(request):
    if request.user.groups.filter(name='administrador').exists():
        return render(request, 'gerente/indexGerente.html', {})
    else:
        return render(request, 'caja/indexcaja.html', {})

@login_required
def verinventario(request):
    insumo = Insumo.objects.all().order_by('existencia')
    existencias = Existencia.objects.all()
    contexto = {'existencias': existencias, }
    if request.user.groups.filter(name='administrador').exists():
        return render(request, 'gerente/verInventario.html', contexto)
    else:
        return render(request, 'caja/indexcaja.html', {})


@login_required
def gestinsumo(request,idInsumo):
    if request.method=='POST':
        formulario=agregarExistencia(request.POST)
        if formulario.is_valid():
            form_data=formulario.cleaned_data
            insumo = Insumo.objects.get(id=idInsumo)
            existencia = Existencia.objects.get(fkInsumo=idInsumo)
            existencia.aumentar( int(insumo.cantPaquete) * int( form_data.get("cantidad")) )
            existencia.save()
            return redirect('gerente:verinve')
    else:
        formulario=agregarExistencia()
        return render(request, 'gerente/gestionarInsumo.html',{'form':formulario,'idInsumo':idInsumo})

    


@login_required
def addinsumo(request):
    if request.method == 'POST':
        form = insumoForm(request.POST)
        if form.is_valid():
            form.save()
            existencia = Existencia()
            existencia.fkInsumo=Insumo.objects.latest('id')
            existencia.save()
        return redirect('gerente:verinve')
    else:
        form = insumoForm()
    return render(request,'gerente/crearInsumo.html',{'form':form})


@login_required
def estadorestaurant(request):
    mesa = Mesa.objects.all().order_by('id')
    cuenta = Cuenta.objects.all()
    pedido = Pedido.objects.all().order_by('fkCuenta')
    contexto = {'mesas':mesa,'cuentas':cuenta,'pedidos':pedido}
    if request.user.groups.filter(name='administrador').exists():
        return render(request, 'gerente/estadoRestau.html', contexto)
    else:
        return render(request, 'caja/indexcaja.html', {})

@login_required
def grafdinero(request):
    now = datetime.now()
    transaccion = Transaccion.objects.all()
    mes = Mes.objects.all().order_by('id')
    cuenta = Cuenta.objects.all()
    contexto = {'meses': mes, 'cuentas': cuenta, 'transacciones':transaccion,'dia': now}
    if request.user.groups.filter(name='administrador').exists():
        return render(request, 'gerente/estadisticaDinero.html', contexto)
    else:
        return render(request, 'caja/indexcaja.html', {})


@login_required
def grafventas(request):
    mesa = Mesa.objects.all()
    cuenta = Cuenta.objects.all()
    pedido = Pedido.objects.all().order_by('fkCuenta')
    contexto = {'mesas': mesa, 'cuentas': cuenta, 'pedidos': pedido}
    if request.user.groups.filter(name='administrador').exists():
        return render(request, 'gerente/estadisticaVentas.html', contexto)
    else:
        return render(request, 'caja/indexcaja.html', {})

@login_required
def verventas(request):
    cuenta = Cuenta.objects.all().order_by('fechaCuenta')
    contexto = {'cuentas': cuenta, }
    if request.user.groups.filter(name='administrador').exists():
        return render(request, 'gerente/verVentas.html', contexto)
    else:
        return render(request, 'caja/indexcaja.html', {})


@login_required
def detacue(request, idCuenta):
    cuenta = Cuenta.objects.get(id=idCuenta)
    mesa = Mesa.objects.all()
    pedido = Pedido.objects.filter(fkCuenta=cuenta.id)
    linea=[]
    for pedi in pedido:
        lineas = LineaDePedido.objects.filter(fkPedido=pedi.id)
        for lin in lineas:
            linea.append(lin)
    contexto = {'mesas': mesa, 'cuentas': cuenta, 'pedidos': pedido, 'lineas': linea}
    if request.user.groups.filter(name='administrador').exists():
        return render(request, 'gerente/detalleCuenta.html', contexto)
    else:
        return render(request, 'caja/indexcaja.html', {})


@login_required
def generarTickets(request):
    generad=generador()
    cupones=Cupon.objects.all().filter(usado=False)
    contexto={'form':generad,'cupones':cupones}

    if request.method=='POST':
        form=generador(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            for j in range(form_data.get('cantidad')):
                codigo=""
                for i in range(5):
                    a=choice(["0","1","2","3","4","5","6","7","8","9"])
                    codigo=codigo+a
                cupon=Cupon()
                cupon.codigo=codigo
                print(codigo)
                cupon.porcentaje=100
                #a posteriori puede usarse obteniendo el valor del formulario
                cupon.save()
            return redirect('gerente:generador')
    return render(request,'gerente/generador.html',contexto)

@login_required
def elimina1(request,cod):
    Cupon.objects.get(codigo=cod).delete()
    return redirect('gerente:generador')

@login_required
def eliminato2(request):
    Cupon.objects.all().delete()
    return redirect('gerente:generador')

@login_required
def gestmes(request,idMes):
    mes = Mes.objects.get(id=idMes)
    if request.method == 'GET':
        form = transaccionForm(instance=mes)
    else:
        form = transaccionForm(request.POST, instance=mes)
        if form.is_valid():
            form.save()
        return redirect('gerente:indexger')
    return render(request, 'gerente/gestionarMes.html', {'form': form, 'idMes': idMes, 'Mes':mes})

@login_required
def prodDiarios(request):
    now = datetime.now()
    transaccion = Transaccion.objects.all()
    mes = Mes.objects.all().order_by('id')
    cuenta = Cuenta.objects.filter(archivado=True,cancelado=False)    
    pedido = Pedido.objects.all()
    linea = LineaDePedido.objects.all()
    contexto = {'meses': mes, 'cuentas': cuenta, 'pedidos': pedido, 'lineas': linea, 'transacciones':transaccion,'dia': now}
    return render(request, 'gerente/productosVendidosDiarios.html', contexto)


def prodDiarios2(request):
    now = date.today()
    producto = Producto.objects.all()
    cuenta = Cuenta.objects.all().filter(cancelado=False,fechaCuenta=now)
    #pedidos,lineas,cuentas filtrados :v
    listaDiccionariosCuentaPedidos=[]
    for cuent in cuenta:
        diccionarioCuentaPedidos={}
        pedidos = Pedido.objects.filter(fkCuenta=cuent.id)
        LP=[]
        for pedid in pedidos:
            '''para que no se me olvide qué hago, creo un diccionario vacío, obtengo las líneas referentes al pedido, luego creo un diccionario
            que contiene el pedido y las líneas filtradas, luego lo agrego a un array '''
            diccionarioLineasPedido={}
            linea = LineaDePedido.objects.filter(fkPedido=pedid.id,cancelado=False)
            diccionarioLineasPedido['pedido']=pedid
            diccionarioLineasPedido['lineas']=linea
            LP.append(diccionarioLineasPedido)
        '''luego al diccionario vacío al inicio de la iteración le añado los registros que contienen la cuenta y la lista de diccionarios que contienen los pedidos 
        y sus líneas, luego lo añado a una lista '''
        diccionarioCuentaPedidos['cuenta']=cuent
        diccionarioCuentaPedidos['pedidos']=LP
        listaDiccionariosCuentaPedidos.append(diccionarioCuentaPedidos)
    contexto = {'dia': now,'productos':producto,'LPP':listaDiccionariosCuentaPedidos}
    return render(request, 'gerente/productosVendidosTotalesD.html', contexto)

@login_required
def prodDiariosM(request):
    now = date.today()
    producto = Producto.objects.all()
    cuenta = Cuenta.objects.all().filter(cancelado=False,fechaCuenta=now)
    #pedidos,lineas,cuentas filtrados :v
    listaDiccionariosCuentaPedidos=[]
    for cuent in cuenta:
        diccionarioCuentaPedidos={}
        pedidos = Pedido.objects.filter(fkCuenta=cuent.id)
        LP=[]
        for pedid in pedidos:
            '''para que no se me olvide qué hago, creo un diccionario vacío, obtengo las líneas referentes al pedido, luego creo un diccionario
            que contiene el pedido y las líneas filtradas, luego lo agrego a un array '''
            diccionarioLineasPedido={}
            linea = LineaDePedido.objects.filter(fkPedido=pedid.id,cancelado=False)
            diccionarioLineasPedido['pedido']=pedid
            diccionarioLineasPedido['lineas']=linea
            LP.append(diccionarioLineasPedido)
        '''luego al diccionario vacío al inicio de la iteración le añado los registros que contienen la cuenta y la lista de diccionarios que contienen los pedidos 
        y sus líneas, luego lo añado a una lista '''
        diccionarioCuentaPedidos['cuenta']=cuent
        diccionarioCuentaPedidos['pedidos']=LP
        listaDiccionariosCuentaPedidos.append(diccionarioCuentaPedidos)
    contexto = {'dia': now,'productos':producto,'LPP':listaDiccionariosCuentaPedidos}
    return render(request, 'gerente/productosVendidosTotalesM.html', contexto)


@login_required
def registros(request):
    now = date.today()
    transaccion = Transaccion.objects.filter(fecha=now)
    #producto = Producto.objects.all()
   # mes = Mes.objects.all().order_by('id')
    cuenta = Cuenta.objects.all().filter(cancelado=False,fechaCuenta=now)
    #pedido = Pedido.objects.all().filter(modificado=False)#depreciado
    #pedidos,lineas,cuentas filtrados :v
    listaDiccionariosCuentaPedidos=[]
    for cuent in cuenta:
        diccionarioCuentaPedidos={}
        pedidos = Pedido.objects.filter(fkCuenta=cuent.id)
        listaDiccionarioLineasPedido=[]
        for pedid in pedidos:
            '''para que no se me olvide qué hago, creo un diccionario vacío, obtengo las líneas referentes al pedido, luego creo un diccionario
            que contiene el pedido y las líneas filtradas, luego lo agrego a un array '''
            diccionarioLineasPedido={}
            lineas = LineaDePedido.objects.filter(fkPedido=pedid.id)
            diccionarioLineasPedido['pedido']=pedid
            diccionarioLineasPedido['pedidos']=lineas
            listaDiccionarioLineasPedido.append(diccionarioLineasPedido)
        '''luego al diccionario vacío al inicio de la iteración le añado los registros que contienen la cuenta y la lista de diccionarios que contienen los pedidos 
        y sus líneas, luego lo añado a una lista '''
        diccionarioCuentaPedidos['cuenta']=cuent
        diccionarioCuentaPedidos['pedidos']=listaDiccionarioLineasPedido
        listaDiccionariosCuentaPedidos.append(diccionarioCuentaPedidos)
   # linea = LineaDePedido.objects.all()#depreciado
    contexto = { 'cuentas': cuenta,  'transacciones':transaccion,'dia': now}
    return render(request, 'gerente/registros.html', contexto)

@login_required
def addtransaccion(request):
    if request.method == 'POST':
        form = transaccionForm(request.POST)
        if form.is_valid():
            form.save()
        if request.user.groups.filter(name='administrador').exists():
            return redirect('gerente:registrs')
        else:
            return redirect('gerente:proddiarios')
    else:
        form = transaccionForm()
    return render(request,'gerente/agregarTransaccion.html',{'form':form})

@login_required
def eliminaT(request,idTransaccion):
    t=Transaccion.objects.get(id=idTransaccion)
    t.delete()
    if request.user.groups.filter(name='administrador').exists():
        return redirect('gerente:registrs')
    else:
        return redirect('gerente:proddiarios')

@login_required #ver todos los meseros
def meseros(request):
    if request.user.groups.filter(name='administrador').exists():
        meseros = User.objects.filter(groups__name__in=['meseros','cajeros',"supervisores","administrador"])
        return render(request,'gerente/meseros/meseros.html',{'meseros':meseros})
    else:
        return redirect('ingreso:index')

@login_required #se carga el formulario de creación de meseros y su posterior adición al grupo
def signup(request):
    if request.user.groups.filter(name='administrador').exists():
        if request.method == 'POST':
            form = registroMesero(request.POST)
            if form.is_valid():
                try:
                    user = form.save()
                    group = Group.objects.get(id=int(request.POST.get('group')))
                    print(group)
                    user.groups.add(group)
                    user.save()
                    return redirect('gerente:meseros')
                except:
                    form = registroMesero()
                    return render(request, 'gerente/meseros/registro.html', {'form': form}) 
        else:
            form = registroMesero()
        return render(request, 'gerente/meseros/registro.html', {'form': form})
    else:
        return redirect('ingreso:index')
@login_required
def cambiarContrasenia(request,idUsuario):
    if request.user.groups.filter(name='administrador').exists():
        if request.method == 'POST':
            usuario = User.objects.get(id=idUsuario)
            form = PasswordChangeForm(usuario, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user) 
                return redirect('/administrador/meseros')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'gerente/meseros/cambiar_contrasenia.html', {'form': form})
    else:
        return redirect('ingreso:index')

@login_required
def eliminar_usuario(request):
    if request.user.groups.filter(name='administrador').exists():
        if request.method == 'POST':
            usuario = User.objects.get(id=int(request.POST.get('idUsuario')))
            usuario.delete()
        return redirect('/administrador/meseros')
    else:
        return redirect('ingreso:index')
@login_required 
def categorias(request):
    if request.user.groups.filter(name='administrador').exists():
        categorias = CategoriaProducto.objects.all()
        array=[]
        for cat in categorias:
            diccionario={}
            diccionario['categoria']=cat
            diccionario['productos']= Producto.objects.filter(fkCategoriaProducto=cat.id).count()
            array.append(diccionario)
        return render(request,'gerente/categoriaProductos/categorias.html',{'array':array})
    else:
        return redirect('ingreso:index')
@login_required 
def addCategoria(request):
    if request.user.groups.filter(name='administrador').exists():
        if request.method == 'POST':
            form = registroCategoria(request.POST)
            if form.is_valid():                
                form.save()
                return redirect('gerente:categorias')
            else:
                return redirect('gerente:categorias')
        else:
            form = registroCategoria()
            contexto = {'form':form}
            return render(request,'gerente/categoriaProductos/agregar.html',contexto)
    else:
        return redirect('ingreso:index')

@login_required 
def eliminarCategoria(request):
    if request.user.groups.filter(name='administrador').exists():
        if request.method == 'POST':
            cate = CategoriaProducto.objects.get(id=int(request.POST.get('idCategoria')))
            cate.delete()
            return redirect('gerente:categorias')
    else:
        return redirect('ingreso:index')

@login_required 
def editarCategoria(request,idCategoria):
    if request.user.groups.filter(name='administrador').exists():
        categoria = CategoriaProducto.objects.get(id=idCategoria)
        if request.method == 'POST':
            form = registroCategoria(request.POST,instance=categoria)
            if form.is_valid():
                form.save()
                return redirect('gerente:categorias')
            else:
                return redirect('gerente:categorias')
        else:
            form=registroCategoria(instance=categoria)
            contexto = {'form':form}
            return render(request,'gerente/categoriaProductos/agregar.html',contexto)
    else:
        return redirect('ingreso:index')


@login_required
def gestproduct(request,idProducto):
    producto = Producto.objects.get(id=idProducto)
    if request.method == 'GET':
        form = productoForm(instance=producto)
    else:
        form = productoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
        return redirect('gerente:prodc')
    return render(request, 'gerente/gestionarProducto.html', {'form': form, 'idProducto': idProducto, 'Producto':producto})

def product(request):
    if request.user.groups.filter(name='administrador').exists():
        productos = Producto.objects.all().order_by('fkCategoriaProducto')
        return render(request,'gerente/productos/productos.html',{'productos':productos})
    else:
        return redirect('ingreso:index')

@login_required
def eliminaPrd(request,idProducto):
    if request.user.groups.filter(name='administrador').exists():
        t=Producto.objects.get(id=idProducto)
        t.delete()
        return redirect('gerente:prodc')
    else:
        return redirect('ingreso:index')
