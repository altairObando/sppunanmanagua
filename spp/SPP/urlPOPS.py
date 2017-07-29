from django.conf.urls import url
from .views import * 
urlpops = [
        ################# popups busquedas ###########################
    url(r'^PopDocentes/$', popDocentes, name='Pop up'),
    url(r'^PopProyector/$', PopProyector, name='Pop up'),
    url(r'^PopAsignatura/$', PopAsignatura, name='Pop up'),
    ]
