from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.ProductList.as_view(), name='product_list'),
    url(r'^(?P<pk>\d+)/$', views.ProductDetail.as_view(), name='product_detail'),

    url(r'^dashboard/products/$', views.ProductList.as_view(template_name='estore/dashboard_product_list.html', permission_required='estore.change_product'), name='dashboard_product_list'),
    url(r'^dashboard/products/create$', views.ProductCreate.as_view(), name='dashboard_product_create'),
    url(r'^dashboard/products/(?P<pk>\d+)/update$', views.ProductUpdate.as_view(), name='dashboard_product_update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
