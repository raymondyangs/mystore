from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('create', views.ProductCreate.as_view(), name='product_create'),
    path('<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('<int:pk>/update', views.ProductUpdate.as_view(), name='product_update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
