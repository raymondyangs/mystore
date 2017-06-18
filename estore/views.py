from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product


# Create your views here.


def product_list(request):
    products = Product.objects.all()
    return render(request, 'estore/product_list.html', {'products': products})


@permission_required('estore.add_product')
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'estore/product_form.html', {'form': form})


@permission_required('estore.change_product')
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)

    if request.POST and form.is_valid():
        form.save()
        messages.success(request, '產品已變更')

    return render(request, 'estore/product_form.html', {'form': form})
