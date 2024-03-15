from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required





# Create your views here.

def principal(request):
	return render(request,'ingreso/inicio.html')

def auth(request):
	if request.method == 'POST':
		usern=request.POST.get('user',None)
		passw=request.POST.get('pass',None)
		user = authenticate(username=usern,password=passw)
		if user is not None:
			login(request, user)
			return redirect('ingreso:index')
		else:
			return redirect('ingreso:ingresar')
	else:
		return render(request, 'ingreso/inicio.html',{})

@login_required
def index(request):
	if request.user.groups.filter(name='administrador').exists():
		return render(request,'gerente/indexGerente.html',{})
	elif request.user.groups.filter(name='cajeros').exists():
		return redirect('caja:indexcajero')
	elif request.user.is_staff:
		return redirect ('admin:index')
	elif request.user.groups.filter(name='supervisores').exists():
		return redirect('supervisor:indexSupervisor')
	else:
		return render(request,'anothers/indexnope.html',{})