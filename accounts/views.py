from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.views.decorators.http import require_http_methods, require_POST
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, get_user_model
from products.models import Product 


def index(request):
    return render(request, "index.html")

@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("index")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)

@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("index")

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "accounts/signup.html", context)

@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect("index")

@require_http_methods(["GET", "POST"])
def edit(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = UserChangeForm(instance=request.user)
    context = {"form": form}
    return render(request, "accounts/edit.html", context)

@login_required
@require_http_methods(["GET", "POST"])
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("index")
    else:
        form = PasswordChangeForm(request.user)
    context = {"form": form}
    return render(request, "accounts/change_password.html", context)

@login_required
def profile(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    my_products = Product.objects.filter(author=request.user).order_by("-created_at")
    like_products = request.user.like_products.all().order_by("-created_at")
    context = {"member": member, "my_products": my_products, "like_products":like_products,}
    return render(request, "accounts/profile.html", context)

@login_required
def profile_update(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    if request.method == "POST":
        if "reset_image" in request.POST:  
            member.image = None
            member.save()
            return redirect("accounts:profile", member.username)
        form = ProfileImageForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile", member.username)
    else:
        form = ProfileImageForm(instance=member)
    context = {"member": member, "form": form}
    return render(request, "accounts/profile_update.html", context)

@require_POST
def follow(request, user_id):
    if request.user.is_authenticated:
        member = get_object_or_404(get_user_model(), pk=user_id)
        if request.user != member:
            if request.user in member.followers.all():
                member.followers.remove(request.user)
            else:
                member.followers.add(request.user)
        return redirect("accounts:profile", member.username)
    return redirect("accounts:login")
