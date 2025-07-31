from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('reclamation/',views.HomePage,name='reclamation'),
    path('logout/',views.LogoutPage,name='logout'),   
    path('homecitoyen/', views.homecitoyen, name='homecitoyen'),
    #path('home_agent/', views.HomeAgent, name='home_agent'),
    path('save_point/', views.save_point, name='save_point'),
    

]