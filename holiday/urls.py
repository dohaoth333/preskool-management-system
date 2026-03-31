from django.urls import path
from . import views

urlpatterns = [
    # Le chemin pour voir la liste des jours fériés
    path('list/', views.holiday_list, name='holiday_list'),

    # Le chemin pour ajouter un jour férié
    path('add/', views.add_holiday, name='add_holiday'),
    path('edit/<int:id>/', views.edit_holiday, name='edit_holiday'),
    path('delete/<int:id>/', views.delete_holiday, name='delete_holiday'),
]
