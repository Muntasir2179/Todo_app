from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home_page"),
    path('login/', views.login, name="login_page"),
    path('signup/', views.signup, name="signup_page"),
    path('add-todo/', views.add_todo, name="add_todo_page"),
]
