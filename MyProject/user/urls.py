from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('index/', views.home),
    path('about/', views.about),
    path('contactus/', views.contactus),
    path('services/', views.services),
    path('myorders/', views.myorders),
    path('myprofile/', views.myprofile),
    path('product/', views.product),
    path('signup/', views.signup_reg),
    path('signin/', views.login),
    path('prodetails/', views.prodetails),
    path('process/',views.process),
    path('logout/',views.logout),
    path('cart/',views.cart),]




