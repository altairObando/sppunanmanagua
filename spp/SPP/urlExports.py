from django.conf.urls import url
from .views import *
################# controlador de exportaciones ###########################
urlpdfs = [
    url(r'^PDF/$', pdf),
    url(r'Reportes/$', selectReporte, name="Reporte general de prestamos"),
    url(r'Reportes/print/(?P<m1>\d{1,2})/(?P<d1>\d{1,2})/(?P<a1>\d{1,4})/(?P<m2>\d{1,2})/(?P<d2>\d{1,2})/(?P<a2>\d{1,4})/$', export, name="Reporte entre fechas"),
    url(r'Reportes/ReporteEntreFechas/(?P<m1>\d{1,2})/(?P<d1>\d{1,2})/(?P<a1>\d{1,4})/(?P<m2>\d{1,2})/(?P<d2>\d{1,2})/(?P<a2>\d{1,4})/$', ReporteEntreFechas, name="Reporte entre fechas"),
    ]
