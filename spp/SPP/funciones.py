from __future__ import unicode_literals
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .forms import *
from .models import *
from datetime import datetime, date
import pdfkit
def Paginador(request, queryset, num_paginas):
	paginas = Paginator(queryset, num_paginas)
	page = request.GET.get('page')
	try:
		resultado = paginas.page(page)
	except PageNotAnInteger:
		resultado = paginas.page(1)
	except EmptyPage:
		resultado = paginas.page(paginas.num_pages)
	return resultado
def GenerarPDF(request, Ruta, Nombre, Options=None):
	Options = {
    'page-size': 'Letter',
    'encoding': "UTF-8",
    'orientation': 'Landscape',
    'custom-header' : [
        ('Accept-Encoding', 'gzip')
    ],
    'no-outline': None
}
	
	pdf = pdfkit.from_url(Ruta,False, options=Options)
	response = HttpResponse(pdf,content_type="application/pdf")
	response["Content-Disposition"] = "attachment; filename="+Nombre
    	return response
