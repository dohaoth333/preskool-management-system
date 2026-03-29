from django.urls import path
from . import views

urlpatterns = [
    # 1. Le Dashboard de l'étudiant
    path('dashboard/', views.student_dashboard, name='student_dashboard'),

    # 2. La liste de tous les étudiants
    path('list/', views.student_list, name='student_list'),

    # 3. Ajouter un étudiant
    path('add/', views.add_student, name='add_student'),

    # 4. Voir les détails d'un étudiant (par pk)
    path('view/<int:pk>/', views.view_student, name='view_student'),

    # 5. Modifier un étudiant (par pk)
    path('edit/<int:pk>/', views.edit_student, name='edit_student'),

    # 6. Supprimer un étudiant (par pk)
    path('delete/<int:pk>/', views.delete_student, name='delete_student'),
]