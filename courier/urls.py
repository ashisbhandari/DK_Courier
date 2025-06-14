from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('nav/', views.navbar, name='navbar'),
    path('SignUp/', views.signup, name='signup page'),
    path('Login/', views.login, name='login'),
    # path('Admin/', views.dashboard1, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/',views.dashboard,name='check'),
    path('book/',views.bookdoc,name="book Documents"),
    path('edit/<str:cn_no>/', views.book_edit, name='book_edit'),
    path('bills/<str:cn_no>/', views.pkt_pdf, name='pdf'),
    path('billsbank/<str:cn_no>/', views.pkt_pdf1, name='pdf1'),
    path('invoice/', views.invoice, name='invoice'),
    path('bill/', views.courier_bill, name='bills')   
]