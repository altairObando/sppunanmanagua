from django.conf.urls import url, include
from django.contrib import admin
from SPP import urls
from .views import *
from django.conf import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^SPP/', include ('SPP.urls')),
    url(r'^Logout/$', Logout, name="Cerrar sesion"),
    url(r'',login_page, name="Inicio de sesion" )
]
