from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic

from .forms import OrderInfoForm
from .models import Order, Product

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


class ProductAddToCart(generic.DetailView):
    model = Product
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.request.cart.items.add(self.object)

        messages.success(self.request, '已加入購物車')
        return redirect('product_detail', pk=self.object.id)

class CartDetailFromRequest(generic.DetailView):
    def get_object(self):
        return self.request.cart

class OrderDetail(generic.DetailView):
    def get_object(self):
        return get_object_or_404(Order.objects, token=self.kwargs.get('token'))


class OrderCreateCartCheckout(LoginRequiredMixin, generic.CreateView):
    model = Order
    fields = []

    def form_valid(self, form, **kwargs):
        form_orderinfo = kwargs['form_orderinfo'].save()

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.total = self.request.cart.total_price()
        self.object.info = form_orderinfo
        self.object.save()

        for each_item in self.request.cart.items.all():
            self.object.orderitem_set.create(
                title=each_item.title,
                price=each_item.price,
                quantity=1,
            )

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        return self.render_to_response(self.get_context_data(form=form, **kwargs))

    def get_context_data(self, **kwargs):
        if 'form_orderinfo' not in kwargs:
            kwargs['form_orderinfo'] = OrderInfoForm()
        return super(OrderCreateCartCheckout, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        form_orderinfo = OrderInfoForm(request.POST)
        if form.is_valid() and form_orderinfo.is_valid():
            return self.form_valid(form, form_orderinfo=form_orderinfo)
        else:
            return self.form_invalid(form, form_orderinfo=form_orderinfo)

    def get_success_url(self):
        messages.success(self.request, '訂單已生成')
        return reverse('order_detail', kwargs={'token': self.object.token})