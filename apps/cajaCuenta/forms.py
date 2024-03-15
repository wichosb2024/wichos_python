from django import forms
from apps.cajaCuenta.models import *
from django.forms import widgets
from django.forms import fields, CheckboxInput
from django.contrib.auth.models import User, Group

mesa=Mesa.objects.all().filter(disponible="True").order_by('id')
user=usuarios=User.objects.filter(groups__name__in=['meseros','administrador'])

class guardarVenta(forms.Form):
	nombre = forms.CharField(label="", max_length=25,required=False,widget=forms.TextInput(attrs={'placeholder': 'Nombre del cliente'}))
	mesa = forms.ModelMultipleChoiceField(mesa,required=False,label="")
	check = forms.BooleanField(label="",required=False,widget=widgets.CheckboxInput(attrs={"checked": False, "value":False,"class": "checkbox"}))
	check2 = forms.BooleanField(label="",required=False,widget=widgets.CheckboxInput(attrs={"checked": False, "value":False,"class": "checkbox"}))
	valNombre=forms.IntegerField(label="",required=False)
	valMesa=forms.IntegerField(label="",required=False)
	direccion= forms.CharField(label="", max_length=25,required=False,widget=forms.TextInput(attrs={'placeholder': 'Dirección del cliente'}))
	numero = forms.CharField(label="",max_length=8,required=False, min_length=8,widget=forms.TextInput(attrs={'placeholder': 'Telefono del cliente'}))

class formMesas(forms.Form):
	mesa = forms.ModelMultipleChoiceField(mesa, required=True, label="Elija el nuevo numero de mesa")

class cobrar(forms.Form):
	total = forms.IntegerField(required=False)
	paga = forms.IntegerField(required=False)
	vuelto = forms.FloatField(required=False)

class formulario(forms.Form):
	cantidad=forms.IntegerField(label="",required=False, widget=forms.TextInput(attrs={'placeholder': 'Cantidad de platos '}))
	cebollaBase=forms.IntegerField(label="",required=False, widget=forms.TextInput(attrs={'placeholder': 'Cantidad de platos con cebolla gratis'}))
	cebolla=forms.IntegerField(label="",required=False, widget=forms.TextInput(attrs={'placeholder': 'Cantidad de platos con cebolla extra'}))
	aguacate=forms.IntegerField(label="",required=False, widget=forms.TextInput(attrs={'placeholder': 'Cantidad de platos con aguacate extra'}))

class formulario2(forms.Form):
	cantidad=forms.IntegerField(label="",required=False, widget=forms.TextInput(attrs={'placeholder': 'Cantidad de platos '}))
	cebollaBase=forms.IntegerField(label="",required=False, widget=forms.TextInput(attrs={'placeholder': 'Cantidad de platos con cebolla gratis'}))
	cebolla=forms.IntegerField(label="",required=False, widget=forms.TextInput(attrs={'placeholder': 'Cantidad de platos con cebolla extra'}))
	aguacate=forms.IntegerField(label="",required=False, widget=forms.TextInput(attrs={'placeholder': 'Cantidad de platos con aguacate extra'}))

class comentario(forms.Form):
	usuario = forms.ModelMultipleChoiceField(user,required=True,label="")
	comentario=forms.CharField(label="Nota especial",max_length=50,required=False)
	prioridad = forms.BooleanField(label="Prioridad", required=False, widget=widgets.CheckboxInput(attrs={"checked": False, "value": False, "class": "checkbox"}))

class comentarioObligatorio(forms.Form):
	usuario = forms.ModelMultipleChoiceField(user,required=True,label="")
	comentario=forms.CharField(label="Nota especial",max_length=50,required=True)


class pedidoN(forms.Form):
	check = forms.BooleanField(label="",required=False,widget=widgets.CheckboxInput(attrs={"checked": False, "value":False,"class": "checkbox"}))

class confirmar(forms.Form):
	check = forms.BooleanField(label="", required=False, widget=widgets.CheckboxInput(attrs={"checked": False, "value": False, "class": "checkbox"}))
class ticketIngresar(forms.Form):
	valor = forms.CharField(label="", max_length=25,required=True)