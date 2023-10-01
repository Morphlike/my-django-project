from django.contrib import admin
from django.urls import path, include

from .quiz import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("register/", views.user_registration, name="register"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("category/", views.category_page, name="category_page"),
    path('category/<int:pk>/', views.play, name='play'),
    path("addQuestion/", views.addQuestion, name="addQuestion"),
]
