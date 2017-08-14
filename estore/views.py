import uuid

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from .forms import OrderInfoForm
from .models import Cart_Items, Order, OrderItem, Product


# Create your views here.

class CartItemDelete(generic.DeleteView):
    def get_object(self, queryset=None):
        return self.request.cart.cart_items_set.get(id=self.kwargs.get('pk'))

    def get_success_url(self):
        messages.warning(self.request, '成功將 {} 從購物車刪除!'.format(self.object.product.title))
        return reverse('cart_detail')


class CartDetailMixin(object):
    def get_object(self):
        return self.request.cart


class CartDetailFromRequest(CartDetailMixin, generic.DetailView):
    def get_context_data(self, **kwargs):
        context = {
            'quantity_iter': range(1, 6)
        }
        context.update(kwargs)
        return super(CartDetailFromRequest, self).get_context_data(**context)


class CartDelete(CartDetailMixin, generic.DeleteView):
    def get_success_url(self):
        messages.warning(self.request, '已清空購物車')
        return reverse('cart_detail')

    def get(self, request, *args, **kwargs):
        return redirect('cart_detail')


class CartItemUpdate(generic.UpdateView):
    model = Cart_Items
    fields = ['quantity']
    http_method_names = ['post']

    def get_object(self):
        return self.request.cart.cart_items_set.get(id=self.kwargs.get('pk'))

    def get_success_url(self):
        messages.success(self.request, '成功變更數量')
        return reverse('cart_detail')


class OrderDetailMixin(object):
    def get_object(self):
        return self.request.user.order_set.get(token=uuid.UUID(self.kwargs.get('token')))


class OrderDetail(OrderDetailMixin, generic.DetailView):
    pass


class OrderPayWithCreditCard(OrderDetailMixin, generic.DetailView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        self.object.payment_method = 'credit_card'
        self.object.make_payment()
        self.object.save()

        return redirect('order_detail', token=self.object.token)


class OrderCreateCartCheckout(LoginRequiredMixin, generic.CreateView):
    model = Order
    fields = []

    def form_valid(self, form, **kwargs):
        for each_item in self.request.cart.cart_items_set.all():
            if each_item.product.quantity < each_item.quantity:
                if each_item.product.quantity:
                    messages.error(self.request, '{} 庫存不足, 請重新確認該商品數量'.format(each_item.product.title))
                    each_item.quantity = each_item.product.quantity
                    each_item.save()
                else:
                    messages.error(self.request, '{} 已售完, 請重新確認訂單'.format(each_item.product.title))
                    self.request.cart.cart_items_set.remove(each_item)
                return self.form_invalid(form, **kwargs)

        form_orderinfo = kwargs['form_orderinfo'].save()

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.total = self.request.cart.total_price()
        self.object.info = form_orderinfo
        self.object.save()

        for each_item in self.request.cart.cart_items_set.all():
            self.object.orderitem_set.create(
                title=each_item.product.title,
                price=each_item.product.price,
                quantity=each_item.quantity,
            )
            each_item.product.quantity = each_item.product.quantity - each_item.quantity
            each_item.product.save()

        self.request.cart.cart_items_set.all().delete()

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
        self.request.cart.cart_items_set.create(product=self.object, quantity=1)

        messages.success(self.request, '已加入購物車')
        return redirect('product_detail', pk=self.object.id)


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
