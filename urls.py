from django.conf.urls import url

from plugins.ingenta import views

urlpatterns = [
    url(r'^$', views.index, name='ingenta_index'),
]
