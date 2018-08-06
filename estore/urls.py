from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('<int:pk>/addtocart', views.ProductAddToCart.as_view(), name='product_addtocart'),

    path('cart/', views.CartDetailFromRequest.as_view(), name='cart_detail'),
    path('cart/checkout', views.OrderCreateCartCheckout.as_view(), name='cart_checkout'),

    path('dashboard/products/', views.ProductList.as_view(template_name='estore/dashboard_product_list.html', permission_required='estore.change_product'), name='dashboard_product_list'),
    path('dashboard/products/create', views.ProductCreate.as_view(), name='dashboard_product_create'),
    path('dashboard/products/<int:pk>/update', views.ProductUpdate.as_view(), name='dashboard_product_update'),

    path('dashboard/users/', views.UserList.as_view(), name='dashboard_user_list'),
    path('dashboard/users/<int:pk>/addtostaff', views.UserAddToStaff.as_view(), name='dashboard_user_addtostaff'),
    path('dashboard/users/<int:pk>/removefromstaff', views.UserRemoveFromStaff.as_view(), name='dashboard_user_removefromstaff'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
