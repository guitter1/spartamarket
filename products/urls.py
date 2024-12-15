from django.urls import path
from . import views
app_name="products"

urlpatterns = [
    path("", views.products, name="products"),
    path("new/", views.new, name="new"),
    path("<int:pk>/", views.product_detail, name="product_detail"),
    path("<int:pk>/edit/", views.edit, name="edit"),
    path("<int:pk>/delete/", views.delete, name="delete"),
]