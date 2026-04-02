from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Subject
from department.models import Department
from teacher.models import Teacher
from home_auth.decorators import admin_required, admin_or_teacher_required


# 1. Liste des matières — visible par TOUS les utilisateurs connectés
@login_required(login_url='login')
def subject_list(request):
    subjects = Subject.objects.select_related('department', 'teacher').all()
    return render(request, 'subject/subjects.html', {'subjects': subjects})


# 2. Add une matière — ADMIN seulement
@admin_or_teacher_required
def add_subject(request):
    departments = Department.objects.all()
    teachers = Teacher.objects.all()

    if request.method == 'POST':
        subject_code = request.POST.get('subject_code')
        subject_name = request.POST.get('subject_name')
        credits = request.POST.get('credits', 0)
        description = request.POST.get('description', '')
        department_id = request.POST.get('department_id')
        teacher_id = request.POST.get('teacher_id')

        subject = Subject(
            subject_code=subject_code,
            subject_name=subject_name,
            credits=credits,
            description=description,
        )
        if department_id:
            subject.department = Department.objects.get(id=department_id)
        if teacher_id:
            subject.teacher = Teacher.objects.get(id=teacher_id)
        subject.save()

        messages.success(request, 'Subject ajoutée avec succès !')
        return redirect('subject_list')

    return render(request, 'subject/add-subject.html', {
        'departments': departments,
        'teachers': teachers,
    })


# 3. Edit une matière — ADMIN seulement
@admin_or_teacher_required
def edit_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    departments = Department.objects.all()
    teachers = Teacher.objects.all()

    if request.method == 'POST':
        subject.subject_code = request.POST.get('subject_code')
        subject.subject_name = request.POST.get('subject_name')
        subject.credits = request.POST.get('credits', 0)
        subject.description = request.POST.get('description', '')

        department_id = request.POST.get('department_id')
        teacher_id = request.POST.get('teacher_id')
        subject.department = Department.objects.get(id=department_id) if department_id else None
        subject.teacher = Teacher.objects.get(id=teacher_id) if teacher_id else None

        subject.save()
        messages.success(request, 'Subject modifiée avec succès !')
        return redirect('subject_list')

    return render(request, 'subject/edit-subject.html', {
        'subject': subject,
        'departments': departments,
        'teachers': teachers,
    })


# 4. Delete une matière — ADMIN seulement
@admin_or_teacher_required
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    messages.success(request, 'Subject supprimée.')
    return redirect('subject_list')
