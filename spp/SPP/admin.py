from django.contrib import admin
from .models import *
# Register your models here.
class SolicitudAdmin(admin.ModelAdmin):
	list_display = ('id', 'Docente', 'Fecha_solicitud','Estado')
	raw_id_fields = ('Docente',)
	fieldsets = [
	('Informacion del solicitante', {'fields':['Docente','Proyector_solicitado', 'Asignatura']}),
	('Estado de la solicitud',{'fields':['Fecha_solicitud','Hora_solicitud','Estado']})]

class DocenteAdmin(admin.ModelAdmin):
	list_display= ('id','Nombre', 'Apellido')
	search_fields = ("Nombre", "Apellido")
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(Docente, DocenteAdmin)
class Padmin(admin.ModelAdmin):
	list_display= ("id","Solicitud","Fecha_prestamo","Comentarios")
admin.site.register(Prestamo,Padmin)

class eManager(admin.ModelAdmin):
	list_display = ('id', 'Desc')

admin.site.register(Estado, eManager)

class DManager(admin.ModelAdmin):
	list_display = (
		
		"usuario",
		"Fecha_hora",
		"Observacion",
		"Daniado",
		)
admin.site.register(Devolucion)
admin.site.register(Marca_proyector)
admin.site.register(Departamento)
admin.site.register(Carrera)
admin.site.register(Especialidad)
admin.site.register(Asignatura)
admin.site.register(Rango)

class ProyectorAdmin(admin.ModelAdmin):
	list_display=('id', 'Marca','Modelo','Cantidad')
	searchfields =['Marca']
admin.site.register(Proyector, ProyectorAdmin)