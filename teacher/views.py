from django.shortcuts import render, redirect, get_object_or_404
from .models import Teacher, Department

def teacher_list(request):
    # Plus tard, on récupèrera la liste des profs ici
    return render(request, 'teachers/teachers.html')

def add_teacher(request):
    return render(request, 'teachers/add-teacher.html')

def view_teacher(request, teacher_id):
    return render(request, 'teachers/teacher-details.html')

def edit_teacher(request, teacher_id):
    return render(request, 'teachers/edit-teacher.html')

def delete_teacher(request, teacher_id):
    # Plus tard, on mettra la logique de suppression ici
    return redirect('teacher_list')
