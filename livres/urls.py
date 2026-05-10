from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_livres, name='liste_livres'),
    path('ajouter/', views.ajouter_livre, name='ajouter_livre'),
    path('modifier/<int:id>/', views.modifier_livre, name='modifier_livre'),
    path('supprimer/<int:id>/', views.supprimer_livre, name='supprimer_livre'),
    path('rechercher/', views.rechercher_livre, name='rechercher_livre'),
]