from __future__ import unicode_literals
from __future__ import absolute_import
from django.conf.urls import url
from apps.ingreso.views import *
from django.contrib.auth.views import LogoutView
app_name='ingreso'
urlpatterns=[
url(r'^principal/', principal,name="principal"),
url(r'^login/', auth, name="ingresar"),
url(r'^index/', index,name="index"),

url(r'^logout', LogoutView.as_view(next_page='/'), name="logout"),
]