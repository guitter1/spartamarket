from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm
from django.views.decorators.http import require_http_methods, require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

def products(request):
    products=Product.objects.all().order_by("-pk")
    context={"products":products}
    return render(request, "products/products.html", context)

@login_required
def new(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect("products:product_detail", product.id)
    else:
        form = ProductForm()

    context = {"form": form}
    return render(request, "products/new.html", context)

def product_detail(request, pk):
    product=Product.objects.get(pk=pk)
    context={"product":product}
    return render(request, "products/product_detail.html", context)

def edit(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect("products:product_detail", product.pk)
    else:
        form = ProductForm(instance=product)
    context = {
        "form": form,
        "product": product,
    }
    return render(request, "products/edit.html", context)

@require_POST
def delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("products:products")