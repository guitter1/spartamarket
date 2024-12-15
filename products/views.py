from django.shortcuts import render, redirect
from .models import Product, Comment
from .forms import ProductForm, CommentForm
from django.views.decorators.http import require_http_methods, require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .utils import author_required

def products(request):
    products=Product.objects.all().order_by("-pk")
    product_count=products.count()
    context={"products":products, "product_count":product_count}
    return render(request, "products/products.html", context)

@login_required
def new(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author=request.user
            product.save()
            return redirect("products:product_detail", product.id)
    else:
        form = ProductForm()

    context = {"form": form}
    return render(request, "products/new.html", context)

def product_detail(request, pk):
    product=get_object_or_404(Product, pk=pk)
    comment_form=CommentForm()
    comments=product.comments.all().order_by("-pk")
    context={"product":product, "comment_form":comment_form, "comments":comments,}
    return render(request, "products/product_detail.html", context)

@author_required(Product)
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

@author_required(Product)
@require_POST
def delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("products:products")


@require_POST
def comment_create(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.product = product
        comment.author=request.user
        comment.save()
    return redirect("products:product_detail", product.pk)

@author_required(Comment)
@require_POST
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect("products:product_detail", comment.product.pk)