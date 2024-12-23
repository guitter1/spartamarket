from django.shortcuts import render, redirect
from .models import Product, Comment, Hashtag
from .forms import ProductForm, CommentForm, OrderForm, HashtagForm, SearchForm
from django.views.decorators.http import require_http_methods, require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .utils import author_required
from django.db.models import F, Count, Q


def products(request):
    products = Product.objects.annotate(like_count=Count('like_users')) 
    product_count = products.count()
    form = OrderForm(request.GET)

    if form.is_valid():
        category_option = form.cleaned_data.get('category', 'pk')
    else:
        category_option = 'pk'

    if not category_option or category_option == 'pk':  
        products = products.order_by('-pk')  
    elif category_option == 'views':
        products = products.order_by('-views', '-like_count')
    elif category_option == 'like_users':
        products = products.order_by('-like_count', '-views')
    
    search_form = SearchForm(request.GET)
    query = None
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query', '')

        if query:
            products = products.filter(
                Q(title__icontains=query) |         
                Q(content__icontains=query) |      
                Q(author__username__icontains=query) |  
                Q(hashtags__name__icontains=query)  
            ).distinct() 


    context = {"products": products, "product_count": product_count, "form": form, "search_form":search_form}
    return render(request, "products/products.html", context)


@login_required
def new(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()

            hashtags_input = request.POST.get('hashtags', '')  
            if hashtags_input:
                hashtag_names = [tag.strip() for tag in hashtags_input.split(',')]
                for tag_name in hashtag_names:
                    hashtag, _ = Hashtag.objects.get_or_create(name=tag_name)
                    product.hashtags.add(hashtag)

            return redirect("products:product_detail", product.id)
    else:
        form = ProductForm()

    context = {"form": form}
    return render(request, "products/new.html", context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Product.objects.filter(pk=pk).update(views=F('views') + 1)
    hashtag_form = HashtagForm()
    comment_form = CommentForm()
    comments = product.comments.all().order_by("-pk")
    context = {
        "product": product,
        "comment_form": comment_form,
        "comments": comments,
        "hashtag_form": hashtag_form,
    }
    return render(request, "products/product_detail.html", context)

@author_required(Product)
def edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()

            hashtags_input = form.cleaned_data.get('hashtags', '')
            if hashtags_input:
                product.hashtags.clear() 
                hashtag_names = [tag.strip() for tag in hashtags_input.split(',') if tag.strip()]
                for tag_name in hashtag_names:
                    hashtag, _ = Hashtag.objects.get_or_create(name=tag_name)
                    product.hashtags.add(hashtag) 

            return redirect("products:product_detail", product.pk)
    else:
        existing_hashtags = ', '.join(product.hashtags.values_list('name', flat=True))
        form = ProductForm(instance=product, initial={"hashtags": existing_hashtags})

    context = {"form": form, "product": product}
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

@require_POST
def like(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if product.like_users.filter(pk=request.user.pk).exists():
            product.like_users.remove(request.user)
        else:
            product.like_users.add(request.user)
    else:
        return redirect("accounts:login")
    return redirect("products:product_detail", product.pk)

@require_POST
def hashtag(request, pk):
    hashtag_form = HashtagForm(request.POST)
    product = get_object_or_404(Product, pk=pk)
    if hashtag_form.is_valid():
        hashtag_name = hashtag_form.cleaned_data['name']
        hashtag, _ = Hashtag.objects.get_or_create(name=hashtag_name)
        product.hashtags.add(hashtag)

    return redirect("products:product_detail", product.pk)