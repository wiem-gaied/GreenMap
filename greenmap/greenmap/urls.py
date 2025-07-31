from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('accueil/',views.accueil,name='accueil'),
    path('accueil/reclamationsrealisees/',views.reclamationsrealisees,name='reclamationsrealisees'),
    path('accueil/mesreclamation/',views.mesreclamation,name='mesreclamation'),
    path('accueil/mesreclamation/ADDreclamation',views.ADDreclamation,name='ADDreclamation'),
    path('logout/',views.LogoutPage,name='LogoutPage'),   
    #path('home_agent/', views.HomeAgent, name='home_agent'),
    path('save_point/', views.save_point, name='save_point'),
    

]