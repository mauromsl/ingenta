from django.urls import re_path

from plugins.ingenta import views

urlpatterns = [
    re_path(r'^$', views.index, name='ingenta_index'),
]
