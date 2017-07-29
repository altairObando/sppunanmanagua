from __future__ import unicode_literals
from .popviews import *

@login_required(redirect_field_name='Loggin/')
def Home(request):
	pend = Solicitud.objects.filter(Estado = Estado.objects.get(Desc__icontains="Pendiente")).count() + Solicitud.objects.filter(Estado = Estado.objects.get(Desc__icontains="Aprobado")).count()  # Numero de solicitudes pendientes
	f1 = Solicitud.objects.all().count()
	f2 = Prestamo.objects.all().count()  # Numero de prestamos
	f3 = Devolucion.objects.all().count()
	cant = Proyector.Total.total() - f2  # Existencias - Prestados
	return render(request, 'Home.html', {"pro": cant, "f1": f1, "f2": f2, "f3": f3, "pend": pend})

@login_required()
@permission_required('staff')
def tablas(request):
	pro = Proyector.objects.all()
	sol = Solicitud.objects.all()
	doc = Docente.objects.all()	
	return render(request, 'Tablas.html', {
		'doc': doc[:10], 'cantd': doc.count(),
		'pro': pro[:10], 'cantp': pro.count(),
		'sol': sol[:10], 'cants': sol.count()
		})

def viewProyector(request):
	proyectores = Paginador(request, Proyector.objects.filter(estado=True).order_by("Marca", "Modelo"), 10)
	return render(request, "Proyectores.html", {"pro": proyectores})

@login_required(redirect_field_name='Loggin/')
@permission_required('proyectores.Proyector')
def addProyector(request):
	if request.method == 'POST':
		form = frmProyectores(request.POST)
		if form.is_valid():
			datos = form.cleaned_data
			nuevo = Proyector(Marca=datos["Marca"], Cantidad=datos["Cantidad"], Modelo=datos["Modelo"], estado=True)
			nuevo.save()
			return redirect(viewProyector)
	else:
		form = frmProyectores()
	return render(request,'addProyector.html', {'form': form})

@login_required(redirect_field_name='Loggin/')
def editarProyector(request, idProyector):
	try:
		idd = int(idProyector)
		pro = Proyector.objects.get(id=idd)
		marcas = Marca_proyector.objects.all()
		if request.method == "POST":
			form = frmProyectores(request.POST, request.FILES)
			if form.is_valid():
				t = form.cleaned_data
				pro.Marca = t["Marca"]
				pro.Cantidad = t["Cantidad"]
				pro.Modelo = t["Modelo"]
				pro.save()
				return redirect(viewProyector)
		else:
			form = frmProyectores()
		return render(request, 'editproyector.html', {'form': form, 'data': pro, 'marcas': marcas})
	except ValueError:
		return HttpResponse("No se pudo obtener el identificador correcto")
@login_required(redirect_field_name='Loggin/')
def deleteProyector(request, idProyector):
	try:
		cod = int(idProyector)
		pro = Proyector.objects.get(id=cod)
		if request.method == "POST":
			pro.estado = False
			pro.save()
			return redirect(viewProyector)
		else:
			return render(request, 'delProyector.html', {'pro': pro})
	except ValueError:
		return HttpResponse("No se pudo obtener el identificador correcto")

@login_required(redirect_field_name='Loggin/')
def viewDocentes(request):
	docentes = Paginador(request, Docente.objects.filter(Activo=True).order_by("Nombre"), 10)
	return render(request, "Docentes.html", {"docs": docentes})

@login_required(redirect_field_name='Loggin/')
def addDocente(request):
	if request.method == "POST":
		form = frmDocentes(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect(viewDocentes)
	else:
		form = frmDocentes()
	return render(request, 'addDocente.html', {'form': form})
@login_required(redirect_field_name='Loggin/')
def editDocente(request, idDoc):
	try:
		idD = int(idDoc)
		eDoc = Docente.objects.get(id=idD)
		if request.method == "POST":
			form = frmDocentes(request.POST, request.FILES)
			if form.is_valid():
				form.save()
				return redirect(viewDocentes)
		else:
			form = frmDocentes2()
		return render(request, 'editDocente.html', {'form': form, 'datos': eDoc})
	except Exception as e:
		raise e
		return HttpResponse(str(e))
@login_required(redirect_field_name='Loggin/')
def delDocente(request, idDoc):
	try:
		cod = int(idDoc)
		docente = Docente.objects.get(id=cod)
		if request.method == "POST":
			docente.Activo = False
			docente.save()
			return redirect(viewDocentes)
		else:
			return render(request,'delDocente.html', {'datos': docente})
	except ValueError:
		return HttpResponse("No se pudo obtener el identificador correcto")
@login_required(redirect_field_name='Loggin/')
def viewSolicitud(request):
	try:
		if request.method == 'POST':
			select = selectEstados(request.POST)
			if select.is_valid():
				sel = select.cleaned_data
				est = Estado.objects.get(Desc=sel["option"])
				solicitudes = Paginador(request,Solicitud.objects.filter(Estado=est).order_by("Fecha_solicitud"), 10)
				cant = Solicitud.objects.filter(Estado=est).count()
				errors = None
				if cant > 0:
					errors = False
				else:
					errors = True
				return render(request, 'Solicitudes.html', {"sol":solicitudes, "form":select, "errors": errors})
		else:
			form = selectEstados()
			solicitudes = Paginador(request,Solicitud.objects.all().order_by("Fecha_solicitud"), 10)
		return render(request, 'Solicitudes.html', {"sol": solicitudes, "form":form})
	except Exception as e:
		return HttpResponse("%s %s" %(e, "\nLa pagina solicitada no esta disponible :c"))
@login_required(redirect_field_name='Loggin/')
def addSolicitud(request):
	try:
		if request.method == "POST":
			form = Solicitudes(request.POST)
			if form.is_valid():
				data = form.cleaned_data
				doc  = int(data["Docente"])
				pro = int(data["Objeto_solicitado"])
				asig = int(data["Asignatura"])
				nueva = Solicitud(
					Docente = Docente.objects.get(pk=doc),
					Proyector_solicitado= Proyector.objects.get(pk=pro),
					Asignatura = Asignatura.objects.get(pk=asig),
					Fecha_solicitud = data["Fecha"],
					Hora_solicitud = data["Hora"],
					Estado = Estado.objects.get(Desc__icontains="Pendiente")
					)
				nueva.save()
				return redirect(viewSolicitud)
		else:
			form = Solicitudes()
		return render(request, 'addSolicitud.html', {"form":form})
	except Exception as e:
		return HttpResponse(e)

@login_required(redirect_field_name='Loggin/')
def reviewSolicitud(request, idSol):
	try:
		cod = int(idSol)
		query = Solicitud.objects.get(id=cod)
		est = Estado.objects.get(id=query.Estado.id)
		extra = None
		if est.id == 4: ## Si esta prestado mostraremos la informacion del prestamo
			extra = Prestamo.objects.get(Solicitud= query)
		elif est.id == 2:
			extra = Anulacion.objects.get(Solicitud= query)
		return render(request,"view.html", {"data":query,"estado":est, 'info': extra})	
	except Exception, e:
		return HttpResponse(e)
def anular(request, idSol):
	try:
		cod = int(idSol)
		query = Solicitud.objects.get(id=cod)
		est = Estado.objects.get(Desc__icontains="Anulado")
		query.Estado = est
		query.save()
		return redirect(viewSolicitud)
	except Exception as e:
		return HttpResponse("Error en la anulacion")
@login_required(redirect_field_name='Loggin/')
def viewPrestamos(request):
	try:
		query = Prestamo.objects.all().order_by("Fecha_prestamo")
		prestamos = Paginador(request, query, 10)
		if request.method == "POST":
			form = filtroFecha(request.POST)
			if form.is_valid():
				data = form.cleaned_data
				date1 = data["Inicial"]
				date2 = data["Final"]
				query = Prestamo.objects.filter(Fecha_prestamo__range=(date1, date2))
				prestamos = Paginador(request, query.order_by("Fecha_prestamo"), 10)
		else:
			form = filtroFecha()
		return render(request,'Prestamos.html', {'Prestamos': prestamos, "form":form})
	except Exception as e:
		return HttpResponse("Error : %s" %e)
@login_required(redirect_field_name='Loggin/')
def addPrestamo(request, idsolicitud):
	try:
		idsol = int(idsolicitud)
		sol = Solicitud.objects.get(id=idsol)
		pro = Proyector.objects.get(id=sol.Proyector_solicitado.id)
		c = pro.Cantidad
		if request.method == "POST":
			form = frmPrestamo(request.POST)
			if form.is_valid():
				datos = form.cleaned_data
				ux = User.objects.get(username__icontains=request.session["Usuario"])
				nprestamo = Prestamo(
					Solicitud = datos["No_solicitud"],
					usuario = ux,
					Fecha_prestamo = datetime.now().date(),
					Hora= datetime.now().time(),
					Comentarios = datos["Comentarios"]
					)
				nprestamo.save()
				sol.Estado = Estado.objects.get(Desc__icontains="Prestado")
				sol.save()
				return redirect(viewSolicitud)
		else:
			form = frmPrestamo()
		return render(request,"addPrestamo.html", {"form":form,"data":sol, "Disp": c, "Solicitudes": Solicitud.objects.exclude(Estado=Estado.objects.get(Desc__icontains="Prestado"))})
	except Exception as e:
		return HttpResponse(e)
@login_required(redirect_field_name='Loggin/')
def fullPrestamo(request):
	try:
		if request.method == "POST":
			form = formFull(request.POST)
			if form.is_valid():
				data = form.cleaned_data
				doc  = int(data["Docente"])
				pro = int(data["Objeto_solicitado"])
				asig = int(data["Asignatura"])
				nSolicitud = Solicitud(
					Docente = Docente.objects.get(pk=doc),
					Proyector_solicitado= Proyector.objects.get(pk=pro),
					Asignatura = Asignatura.objects.get(pk=asig),
					Fecha_solicitud = data["Fecha"],
					Hora_solicitud = data["Hora"],
					Estado = Estado.objects.get(Desc__icontains="Pendiente")
					)
				nSolicitud.save()
				
				ux = User.objects.get(username__icontains=request.session["Usuario"])
				nprestamo = Prestamo(
					Solicitud = nSolicitud,
					usuario = ux,
					Fecha_prestamo = datetime.now().date(),
					Hora= datetime.now().time(),
					Comentarios = data["Comentarios"]
					)
				nprestamo.save()
				nSolicitud.Estado = Estado.objects.get(Desc__icontains="Prestado")
				nSolicitud.save()
		else:
			form = formFull()
		return render(request, 'fullPrestamo.html', {'form': form})
	except Exception as e:
		return HttpResponse ("Error: %s" %e)
@login_required(redirect_field_name="Loggin/")
def viewDevolucion(request):
	try:
		query = Devolucion.objects.all().order_by("Fecha")
		devs = Paginador(request, query, 10)
		if request.method == "POST":
			form = filtroFecha(request.POST)
			if form.is_valid():
				data = form.cleaned_data
				date1 = data["Inicial"]
				date2 = data["Final"]
				query = Devolucion.objects.filter(Fecha__range=(date1,date2))
				devs = Paginador(request, query,10)
		else:
			form = filtroFecha()
		return render(request,"Devolucion.html", {"Devoluciones": devs, "form":form})
	except Exception, e:
		return HttpResponse("Sitio no encontrado")
@login_required
def addDevolucion(request, idPrestamo):
	try:
		idp  = int(idPrestamo) #Obtenemos el id concreto
		prest = Prestamo.objects.get(Solicitud=Solicitud.objects.get(pk=idp))
		if request.method == "POST":
			user = User.objects.get(username__icontains=request.session["Usuario"])
			form = formDevolucion(request.POST)
			if form.is_valid():
				data = form.cleaned_data
				dev = Devolucion(
					Prestamo = prest,
					Proyector = prest.Solicitud.Proyector_solicitado,
					usuario = user,
					Fecha = datetime.date(datetime.now()),
					Hora = datetime.time(datetime.now()),
					Observacion = data["Observacion"],
					Daniado = data["Daniado"]
				)
				dev.save()
				return redirect(viewPrestamos)
		else:
			form = formDevolucion()
		return render(request, 'addDevolucion.html',{'data': prest, 'form': form})
	except Exception as e:
		return  HttpResponse("Error al devolver proyector \n %s" %e)
@login_required(redirect_field_name="Loggin/")
def newDevolucion(request):
	try:
		if request.method=="POST":
			user = User.objects.get(username__icontains=request.session["Usuario"])
			form = formDevolucion(request.POST)
			if form.is_valid():
				data = form.cleaned_data
				prest = Prestamo.objects.get(id=data["Prestamo"])
				dev = Devolucion(
					Prestamo=data["Prestamo"],
					Proyector=prest.Solicitud.Proyector_solicitado,
					usuario=user,
					Fecha=datetime.date(datetime.now()),
					Hora=datetime.time(datetime.now()),
					Observacion=data["Observacion"],
					Daniado=data["Daniado"]
				)
				dev.save()
				return redirect(viewPrestamos)
		else:
			form = formDevolucion()
		return render(request,"addDevolucion.html", {"form": form})
	except Exception as e:
		pass