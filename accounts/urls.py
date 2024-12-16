from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("delete/", views.delete, name="delete"),
    path("edit/", views.edit, name="edit"),
    path("password/", views.change_password, name="change_password"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profile_update/<str:username>/", views.profile_update, name="profile_update"),
    path("<int:user_id>/follow/", views.follow, name="follow")
]