from django.urls import path
from . import views
app_name="products"

urlpatterns = [
    path("", views.products, name="products"),
    path("new/", views.new, name="new"),
    path("<int:pk>/", views.product_detail, name="product_detail"),
    path("<int:pk>/edit/", views.edit, name="edit"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/comments/", views.comment_create, name="comment_create"),
    path("<int:pk>/comments_delete/", views.comment_delete, name="comment_delete"),
    path("<int:pk>/like/", views.like, name="like"),
]