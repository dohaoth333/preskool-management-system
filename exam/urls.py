from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('add/', views.add_exam, name='add_exam'),
    path('results/add/', views.add_result, name='add_result'),
    path('results/', views.result_list, name='result_list'), 
    path('mes-notes/', views.my_results, name='my_results'),
    path('edit/<int:exam_id>/', views.edit_exam, name='edit_exam'),
    path('delete/<int:exam_id>/', views.delete_exam, name='delete_exam'),
]