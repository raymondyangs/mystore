from django.urls import path

from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create', views.product_create, name='product_create'),
    path('<int:pk>/update', views.product_update, name='product_update'),
]
