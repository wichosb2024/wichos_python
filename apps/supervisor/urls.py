from __future__ import unicode_literals
from __future__ import absolute_import
from django.conf.urls import url
from apps.supervisor.views import *
app_name='supervisor'
urlpatterns=[
    url(r'^verEstadoSupervisor/', verEstadoSupervisor, name="verEstadoSupervisor"),
    url(r'^cambiarEstadoMesa/(?P<idMesa>\w+)', cambiarEstadoMesa, name="cambiarEstadoMesa"),
    url(r'^indexSupervisor/', indexSupervisor, name="indexSupervisor"),
]