from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),          # Home Page
    path('login/', views.login_page, name='login'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('books/', views.index, name='index'),
    path('owner/', views.owner, name='owner'),  # Admin Dashboard
    path('userhome/', views.userhome, name='userhome'),  # User Home Page
    path('add/', views.add_book, name='add_book'),
    path('edit/<int:id>/', views.edit_book, name='edit_book'),
    path('delete/<int:id>/', views.delete_book, name='delete_book'),
    path('register/', views.register_page, name='register'),
    path('users/', views.users_list, name='users_list'),
]