from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('nav/', views.navbar, name='navbar'),
    path('SignUp/', views.signup, name='navbar'),
    path('Login/', views.login_user, name='login'),
    path('Admin/', views.dashboard, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/',views.check,name='check'),
    path('book/',views.bookdoc,name="book Documents"),
    path('book/edit/<int:pk>/', views.book_edit, name='book_edit'),


    
]
