from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.teacher_list, name='teacher_list'),
    path('add/', views.add_teacher, name='add_teacher'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('delete/<int:id>/', views.delete_teacher, name='delete_teacher'),
    path('edit/<int:id>/', views.edit_teacher, name='edit_teacher'),
    # La route pour voir les détails d'un prof :
    path('view/<int:id>/', views.view_teacher, name='view_teacher'),

]