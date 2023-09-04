from django.urls import path

from tokens import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("info", views.info, name="info"),
]
