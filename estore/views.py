from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.views import generic

from .models import Product


# Create your views here.


class ProductList(PermissionRequiredMixin, generic.ListView):
    model = Product

    def has_permission(self):
        if self.permission_required:
            return super(ProductList, self).has_permission()
        else:
            return True


class ProductDetail(generic.DetailView):
    model = Product


class ProductCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'estore.add_product'
    model = Product
    fields = ('title', 'description', 'quantity', 'price', 'image')

    def get_success_url(self):
        messages.success(self.request, '產品已新增')
        return reverse('dashboard_product_list')


class ProductUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'estore.change_product'
    model = Product
    fields = ('title', 'description', 'quantity', 'price', 'image')

    def get_success_url(self):
        messages.success(self.request, '產品已變更')
        return reverse('dashboard_product_update', kwargs=self.kwargs)


class UserList(PermissionRequiredMixin, generic.ListView):
    permission_required = 'auth.change_user'
    model = User
    template_name = 'estore/dashboard_user_list.html'


class UserAddToStaff(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'auth.change_user'
    model = User
    fields = []

    def get_success_url(self):
        if self.request.method == 'POST':
            group = Group.objects.get(name='estore_staff')
            group.user_set.add(self.object)
            messages.success(self.request, '已變更使用者身份為管理者')
        return reverse('dashboard_user_list')


class UserRemoveFromStaff(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'auth.change_user'
    model = User
    fields = []

    def get_success_url(self):
        if self.request.method == 'POST':
            group = Group.objects.get(name='estore_staff')
            group.user_set.remove(self.object)
            messages.success(self.request, '已變更使用者身份為一般使用者')
        return reverse('dashboard_user_list')
