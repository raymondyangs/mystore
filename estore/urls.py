from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.ProductList.as_view(), name='product_list'),
    url(r'^create$', views.ProductCreate.as_view(), name='product_create'),
    url(r'^(?P<pk>\d+)/update$', views.ProductUpdate.as_view(), name='product_update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
