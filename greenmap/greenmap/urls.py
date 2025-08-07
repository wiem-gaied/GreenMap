from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.choisir,name='choisir'),
    path('login_agent/', views.login_agent, name='login_agent'),
    path('login_citoyen/', views.login_citoyen, name='login_citoyen'),
    path('signup_citoyen/', views.signup_citoyen, name='signup_citoyen'),
    path('signup_agent/', views.signup_agent, name='signup_agent'),
    path('mesreclamations/',views.mesreclamation,name='mesreclamations'),
    path('carte/save-point/', views.save_point, name='save_point'),
    path('mesreclamations/supprimer/<int:id>/', views.supprimer_reclamation, name='supprimer_reclamation'),
    path('reclamation/modifier/<int:id>/', views.modifier_reclamation, name='modifier_reclamation'),
    path('Reclamations/',views.AgentReclamations,name='AgentReclamations'),
    path('accueil/mesreclamation/ADDreclamation',views.ADDreclamation,name='ADDreclamation'),
    path('logout/',views.LogoutPage,name='LogoutPage'),
    path('agent/reclamations/modifier-etat/<int:reclamation_id>/', views.modifier_etat_reclamation, name='modifier_etat_reclamation'),
    path('reclamation/<int:reclamation_id>/', views.reclamation_detail, name='reclamation_detail'),

    

    #path('login/',views.LoginPage,name='login'),
    #path('accueil/',views.accueil,name='accueil'),
    #path('accueil/reclamationsrealisees/',views.reclamationsrealisees,name='reclamationsrealisees'),
    #path('accueil/mesreclamation/',views.mesreclamation,name='mesreclamation'),
    
       
    #path('home_agent/', views.HomeAgent, name='home_agent'),
    #path('agent/reclamations/', views.AgentReclamations, name='agent_reclamations'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)