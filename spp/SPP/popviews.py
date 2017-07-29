from .funciones import *
from django.core.urlresolvers import reverse
def pdf(request):
	return GenerarPDF(request,'http://localhost:81/SPP/Proyectores/', 'Docentes.pdf')

def popDocentes(request):
	try:
		if request.method == "POST":
			form =  filtroDocente(request.POST)
			if form.is_valid():
				nombre = form.cleaned_data["doc"]
				docentes = Paginador(request,Docente.objects.filter(Activo=True, Nombre__icontains=nombre).order_by("Nombre"), 10 )
		else:
			docentes = Paginador(request,Docente.objects.filter(Activo=True).order_by("Nombre"), 10 )
			form = filtroDocente()
		return render(request,"popDocente.html", {"docs": docentes, "form":form} )
	except Exception as e:
		return HttpResponse("Error: %s" %e)

def PopProyector(request):
	try:
		filtrado = False
		if request.method == "POST":
			form =  filtroDocente(request.POST)
			if form.is_valid():
				nombre = form.cleaned_data["doc"]
				proyectores = Paginador(request,Proyector.objects.filter(Marca__Marca__icontains = nombre, estado=True, Cantidad__gt=0).order_by("Cantidad"), 10 )
				filtrado = True
		else:
			proyectores = Paginador(request, Proyector.objects.filter(estado=True).order_by("Marca","Modelo"), 10 )
			form = filtroDocente()
		return render(request,"popProyector.html", {"pro": proyectores, "form":form,'filtrado':filtrado} )
	except Exception as e:
		return HttpResponse("Error: %s" %e)

def PopAsignatura(request):
	try:
		if request.method == "POST":
			form =  filtroDocente(request.POST)
			if form.is_valid():
				nombre = form.cleaned_data["doc"]
				asig = Paginador(request,Asignatura.objects.filter(Nombre__icontains=nombre).order_by("Nombre"), 5 )
		else:
			asig = Paginador(request,Asignatura.objects.all().order_by("Nombre"), 5 )
			form = filtroDocente()
		return render(request,"popAsignatura.html", {"asig": asig, "form":form} )
	except Exception as e:
		return HttpResponse("Error: %s" %e)

def selectReporte(request):
	try:
		query =Devolucion.objects.all().order_by("Fecha")
		dev  = Paginador(request, query, 20)
		date1= query[0].Fecha
		date2 = datetime.date(datetime.now())
		if request.method == "POST":
			form = filtroFecha(request.POST)
			if form.is_valid():
				d = form.cleaned_data
				date1 = d["Inicial"]
				date2 = d["Final"]
				query = Devolucion.objects.filter(Fecha__range=(date1, date2))
				dev = Paginador(request, query, 20)
		else:
			form = filtroFecha()
		return render(request, 'Reportes.html', {"data": dev, "form":form,"f1": date1, "f2": date2})
	except Exception as e:
		return HttpResponse ("Error al procesar la informacion %s"%e)
def export(request, m1, d1, a1, m2, d2, a2):
	try:
		date1 = datetime.date(datetime(int(a1),int(m1),int(d1)))
		date2 = datetime.date(datetime(int(a2),int(m2),int(d2)))
		query = Devolucion.objects.filter(Fecha__range=(date1,date2))
		return render(request, 'reporte.html', {'data': query})
	except Exception as e:
		return HttpResponse("Error puto >:v \n%s"%e)
def ReporteEntreFechas(request, m1, d1, a1, m2, d2, a2):
	return GenerarPDF(request, 'http://localhost:81/SPP/Reportes/print/'+m1+"/"+d1+"/"+a1+"/"+m2+"/"+d2+"/"+a2+"/", "Reporte.pdf")