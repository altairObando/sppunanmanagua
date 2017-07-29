from django.contrib.auth.models import User
from django import forms
from .models import *
from datetime import *

class filtroFecha(forms.Form):
    Inicial = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    Final = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
class filtroDocente(forms.Form):
    doc = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}))
class Departamento(forms.Form):
    Nombre=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Mision=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'false'}))
    Vision=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'false'}))
    Historia=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','required':'false'}))
    Ubicacion=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'false'}))
    Organizacion=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'false'}))

class Carrera(forms.Form):
    Nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

class Especialidades(forms.Form):
    Descripcion =forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

class frmDocentes2(forms.Form):
    Nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    Telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Informacion_adicional = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'false'}))
    Foto = forms.ImageField(widget=forms.FileInput(attrs={'class':'file','required':'False'}))
    Activo = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'checkbox', 'required': 'False'}))
class frmDocentes(forms.ModelForm):
    class Meta:
        model = Docente
        fields = ["Nombre","Apellido","Especialidad",
        "Telefono","Informacion_adicional","Foto"]

class Marcas(forms.Form):
    Marca = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

class frmProyectores(forms.Form):
    Marca = forms.ModelChoiceField(queryset=Marca_proyector.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    Modelo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Cantidad = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))

class frmEstados(forms.Form):
    Descripcion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

class selectEstados(forms.Form):
    option = forms.ModelChoiceField(queryset=Estado.objects.all(), widget=forms.Select(attrs={"class":"form-control"}))

class Solicitudes(forms.Form):
    Docente = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Objeto_solicitado = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Asignatura = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Fecha = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    Hora = forms.TimeField(widget=forms.DateInput(attrs={'class':'form-control', 'type': 'time'}))
    
query = Solicitud.objects.all()
query2 = Estado.objects.filter(Desc__icontains="Prestado")
query = query.exclude(Estado=query2)
class frmPrestamo(forms.Form):
    No_solicitud = forms.ModelChoiceField(queryset= query,widget=forms.Select(attrs={'class':'form-control'}))
    Autorizado_por = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'false'}))
    Comentarios = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control', 'required': "False"}))
class formFull(forms.Form):
    Docente = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Objeto_solicitado = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Asignatura = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Fecha = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    Hora = forms.TimeField(widget=forms.DateInput(attrs={'class':'form-control', 'type': 'time'}))

    ### Datos del prestamo ###
    Comentarios = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control', 'required': "False"}))


class formDevolucion(forms.ModelForm):
    class Meta:
        model = Devolucion
        fields = ["Prestamo","Observacion", "Daniado"]