from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.product_list, name='product_list'),
    url(r'^create$', views.product_create, name='product_create'),
    url(r'^(?P<pk>\d+)/update$', views.product_update, name='product_update'),
]
