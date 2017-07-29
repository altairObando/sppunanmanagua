from django.conf.urls import url, include
from .views import *
from urlPOPS import urlpops
from urlExports import urlpdfs
urlpatterns = [
    url(r'^$', Home,name="Pagina de inicio"),
    url(r'^Tablas', tablas, name="Vista rapida de los datos"),
    ################# Proyectores ###########################
    url(r'^Proyectores/$', viewProyector, name="Lista de Proyectores"),
    url(r'^Proyectores/addProyector/$', addProyector, name="Agregar proyector"),
    url(r'^Proyectores/editarProyector/(?P<idProyector>\d{1,3})/$', editarProyector, name="Editar"),
    url(r'^Proyectores/delProyector/(?P<idProyector>\d{1,3})', deleteProyector, name="Eliminar"),
    ################# Docentes ###########################
    url(r'^Docentes/$', viewDocentes, name="Vista docentes"),
    url(r'^Docentes/addDocente/$', addDocente, name="Ingresa un nuevo docente"),
    url(r'^Docentes/editDocente/(?P<idDoc>\d{1,3})/$', editDocente ),
    url(r'^Docentes/delDocente/(?P<idDoc>\d{1,3})/$', delDocente ),
    ################# Solicitudes ###########################
    url(r'^Solicitudes/$', viewSolicitud, name="Filtro de las solicitudes"),
    url(r'^addSolicitud/$', addSolicitud, name="Formulario de solicitudes"),
    url(r'^Solicitudes/view/(?P<idSol>\d{1,3})/$',reviewSolicitud, name="Revision de una solicitud" ),
    url(r'^Anular/(?P<idSol>\d{1,3})/$', anular, name="Marca una solicitud como anulada"),
    ################# Prestamos ###########################
    url(r'^Prestamo/(?P<idsolicitud>\d{1,3})/$',addPrestamo, name="Efectuar prestamo" ),
    url(r'^Prestamo/$', viewPrestamos, name='Prestamos efectuados'),
    url(r'^Prestamo/Nuevo/$', fullPrestamo, name="Registrar un prestamo"),
    ################# Devoluciones ###########################
    url(r'^Devoluciones/$', viewDevolucion, name="Lista de las devoluciones efectuadas"),
    url(r'^Devoluciones/nuevo/(?P<idPrestamo>\d{1,3})/$', addDevolucion, name="Registrar una devolucion"),
    url(r'^Devoluciones/view/(?P<idDev>\d{1,3})/$', viewDevolucion, name="Lista de las devoluciones efectuadas"),
    url(r'^Devoluciones/nuevo/$', newDevolucion, name="Registrar una devolucion")

] + urlpops + urlpdfs
