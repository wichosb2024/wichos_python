from apps.cajaCuenta.models import *
from django import forms
from apps.cajaCuenta.models import *
from apps.cajaAdmin.models import *
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields, CheckboxInput
from django.contrib.auth.models import User, Group
grupos = Group.objects.all()
class agregarExistencia(forms.Form):
	cantidad=forms.IntegerField(required=True)

class productoForm(forms.ModelForm):
	class Meta:
		model=Producto

		fields=[
			'nombreProd',
			'precio',
			'fkCategoriaProducto',
			'abreviatura',
			'imagen',
			]


class insumoForm(forms.ModelForm):
	class Meta:
		model=Insumo

		fields=[
			'nombreIns',
			'cantPaquete',
			'proveedor',
			'paquete'
			]
		labels={
			'nombreIns':'Nombre del Insumo',
			'cantPaquete':'Cantidad que tiene cada paquete',
			'proveedor': 'Proveedor',
			'paquete' : 'Es por paquetes?'
		}
		widgets={
			'nombreIns': forms.TextInput(attrs={'class':'form-control'}),
			'cantPaquete': forms.TextInput(attrs={'class':'form-control'}),
			'proveedor': forms.TextInput(attrs={'class':'form-control'}),
			
		}

class generador(forms.Form):
	opciones = (
		(' 10', ' 10'),
		(' 20', ' 20'),
		(' 30', ' 30'),
		(' 40', ' 40'),
		(' 50', ' 50'),
		(' 60', ' 60'),
		(' 70', ' 70'),
		(' 80', ' 80'),
		(' 90', ' 90'),
		(' 100', ' 100'),
		)
	#porcentaje = forms.ChoiceField(label='Porcentaje',widget=forms.Select,choices=opciones)
	cantidad = forms.IntegerField(label='', widget=forms.TextInput(attrs={'placeholder': 'Cantidad de tickets '}))


class transaccionForm(forms.ModelForm):
	class Meta:
		model = Transaccion

		fields = [
			'monto',
			'descripcion',
			'tipo',
		]
		labels = {
			'monto': 'Monto de la transaccion',
			'descripcion': 'Descripcion de la transaccion',
			'tipo': 'Marque la casilla para registrar EGRESOS o dejela si es un INGRESO',

		}
		widgets = {
			'monto': forms.TextInput(attrs={'class': 'form-control'}),
			'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
			'tipo': forms.CheckboxInput(),
		}
class registroMesero(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre del mesero'}))
	last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Apellidos del mesero'}))
	group = forms.ModelMultipleChoiceField(grupos, required=True, label="Elija el grupo del usuario")
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )
class registroCategoria(forms.ModelForm):
	class Meta:
		model = CategoriaProducto
		fields = [
			'nombreCate',
			'comidaMexicana',
			'cocinaNormal',
		]
		labels = {
			'nombreCate':'Ingrese el nombre de la categoría',
			'comidaMexicana':'Seleccione si es comida mexicana',
			'cocinaNormal':'Seleccione si son tortas o hamburguesas',
		}
		widgets = {
			'nombreCate': forms.TextInput(attrs={'class': 'form-control'}),
			'comidaMexicana': forms.CheckboxInput(),
			'cocinaNormal': forms.CheckboxInput(),
		}