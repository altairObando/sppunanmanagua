from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import date, datetime
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse



class Departamento(models.Model):
	Nombre_dpto = models.CharField(max_length=50)
	Mision = models.CharField(max_length=50, blank=True)
	Vision = models.CharField(max_length=50, blank=True)
	Historia = models.CharField(max_length=50, blank=True)
	Ubicacion = models.CharField(max_length=50, blank=True)
	Organizacion = models.CharField(max_length=50, blank=True)
	def __str__(self):
		return self.Nombre_dpto
class Carrera(models.Model):
	Nombre_carrera = models.CharField(max_length=50)
	def __str__(self):
		return self.Nombre_carrera
class Rango(models.Model):	
	Abreviatura = models.CharField(max_length=20)
	def __str__(self):
		return self.Abreviatura
class Especialidad(models.Model):
	Rango = models.ForeignKey(Rango)
	Carrera = models.ForeignKey(Carrera)
	def __str__(self):
		return ("%s %s" % (self.Rango, self.Carrera))
	class Meta:
		verbose_name_plural  = "Especialidades"
class Docente(models.Model):
	Nombre = models.CharField(max_length=25)
	Apellido = models.CharField(max_length=25)
	Especialidad = models.ForeignKey(Especialidad)
	Telefono = models.IntegerField(null=True)
	Correo = models.EmailField(blank=True, max_length=100)
	Informacion_adicional = models.CharField(max_length=50, blank=True)
	Foto = models.ImageField(blank=True)
	Activo = models.NullBooleanField(null=True)
	Departamento = models.ForeignKey(Departamento)
	def __str__(self):
		return ("%s %s %s" % (self.Especialidad.Rango, self.Nombre , self.Apellido))
	def get_absolute_url(self):
		return redirect("addProyector")
class Marca_proyector(models.Model):
	Marca = models.CharField(max_length=50)
	def __str__(self):
		return self.Marca
	class Meta:
		verbose_name_plural="Marca de proyector"
class manProyector(models.Manager):
	def total(self):
		i = 0
		x = Proyector.objects.all()
		for j in x:
			i = i+j.Cantidad
		return i
class Proyector(models.Model):
	Marca = models.ForeignKey(Marca_proyector)
	Modelo = models.CharField(max_length=100)	
	Cantidad = models.IntegerField()	
	Total = manProyector() #Manager de sobrecarga
	objects = models.Manager() #Manager predeterminado
	estado = models.NullBooleanField(null=True)
	def __str__(self):
		return ("%s %s" %(self.Marca,self.Modelo))
	class Meta:
		verbose_name_plural = "Proyectores"
	def get_absolute_url(self):
		return reverse('Proyectores.views.addProyector', args=[str(self.id)])
class Estado(models.Model):
	Desc = models.CharField(max_length=10)
	def __str__(self):
		return self.Desc
class Asignatura(models.Model):
	Nombre = models.CharField(max_length=120)
	def __str__(self):
		return self.Nombre
class Solicitud(models.Model):
	Docente = models.ForeignKey(Docente)
	Proyector_solicitado = models.ForeignKey(Proyector)
	Asignatura = models.ForeignKey(Asignatura)
	Seccion = models.IntegerField(blank = True, null=True)
	Fecha_solicitud = models.DateField(default=date.today)
	Hora_solicitud = models.TimeField()
	Estado = models.ForeignKey(Estado, blank=True)
	class Meta:
		ordering = ["Fecha_solicitud","Estado"]
		verbose_name_plural ="Solicitudes"
	def __str__(self):
		#return ("%s" %(self.id))
		return ("No. %s  %s  %s  %s " %(self.id, self.Docente, self.Proyector_solicitado, self.Estado))
class Prestamo (models.Model):
	Solicitud = models.OneToOneField(Solicitud)
	usuario = models.ForeignKey(User)
	Fecha_prestamo = models.DateField()
	Hora = models.TimeField(null=True, blank=True)
	Comentarios = models.CharField(max_length=500, blank=True)
	def __str__(self):
		return "%s %s" %(self.id, self.Solicitud.Docente)
		#return "%s %s %s %s %s" %(self.id, self.Solicitud.Docente, self.Solicitud.Proyector_solicitado, self.Solicitud.Asignatura, self.Fecha_prestamo)

	def save(self, *args, **kwargs):
		sol = Solicitud.objects.get(id=self.Solicitud.id)  #Buscamos la referencia hacia la tabla solicitud
		sol.Estado =  Estado.objects.get(Desc__contains='Prestado')# asignamos el nuevo estado
		pro = Proyector.objects.get(id=sol.Proyector_solicitado.id) #
		pro.Cantidad = pro.Cantidad - 1
		pro.save()
		sol.save()
		super(Prestamo, self).save(*args, **kwargs)
		
	class Meta:
		ordering = ["Fecha_prestamo"] 
class Devolucion(models.Model):
	Prestamo = models.OneToOneField(Prestamo)
	Proyector = models.ForeignKey(Proyector)
	usuario = models.ForeignKey(User)
	Fecha = models.DateField(null = True, blank=True)
	Hora = models.TimeField(null = True, blank=True)
	Observacion = models.CharField(max_length = 200, blank=True)
	Daniado = models.NullBooleanField(default = False)
	
	def save(self, *args, **kwargs):
		idest = Estado.objects.get(Desc__contains="Devuelto")
		sol = Solicitud.objects.get(pk=self.Prestamo.Solicitud.id)
		sol.Estado = idest
		pro = Proyector.objects.get(pk=sol.Proyector_solicitado.id)
		if not self.Daniado:
			pro.Cantidad = pro.Cantidad + 1
			pro.save()
		sol.save()
		self.Proyector  = pro
		super(Devolucion, self).save(*args, **kwargs)
	def actualizar(self, *args,**kwargs):
		super(Devolucion, self).save(*args, **kwargs)