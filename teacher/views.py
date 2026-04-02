from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from department.models import Department
from .models import Teacher
from home_auth.decorators import admin_required
from django.contrib import messages

# 1. Liste des professeurs — ADMIN seulement
@admin_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher/teachers.html', {'teachers': teachers})

# Dashboard teacher — accessible au teacher lui-même
def teacher_dashboard(request):
    return render(request, 'teacher/teacher-dashboard.html')

# 2. Add un professeur — ADMIN seulement
@admin_required
def add_teacher(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        teacher_email = request.POST.get('teacher_email')
        teacher_password = request.POST.get('teacher_password')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        mobile_number = request.POST.get('mobile_number')
        joining_date = request.POST.get('joining_date')
        experience = request.POST.get('experience')
        address = request.POST.get('address')
        
        department_id = request.POST.get('department_id')
        department = Department.objects.get(id=department_id)

        teacher = Teacher(
            teacher_id=teacher_id,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            mobile_number=mobile_number,
            joining_date=joining_date,
            experience=experience,
            address=address,
            department=department
        )
        teacher.save()

        # Créer l'utilisateur pour le professeur
        if teacher_email and teacher_password:
            User = get_user_model()
            if not User.objects.filter(username=teacher_email).exists():
                try:
                    user = User.objects.create_user(
                        username=teacher_email,
                        email=teacher_email,
                        password=teacher_password,
                        first_name=first_name,
                        last_name=last_name
                    )
                    user.is_teacher = True
                    user.save()
                except IntegrityError:
                    messages.error(request, 'Un utilisateur avec cet email existe déjà ou une erreur d\'intégrité est survenue.')

        return redirect('teacher_list')

    departments = Department.objects.all()
    return render(request, 'teacher/add-teacher.html', {'departments': departments})

# 3. Delete un professeur — ADMIN seulement
@admin_required
def delete_teacher(request, id):
    teacher = Teacher.objects.get(id=id)
    teacher.delete()
    return redirect('teacher_list')

# 4. Edit un professeur — ADMIN seulement
@admin_required
def edit_teacher(request, id):
    teacher = Teacher.objects.get(id=id)
    departments = Department.objects.all()

    if request.method == 'POST':
        teacher.teacher_id = request.POST.get('teacher_id')
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.gender = request.POST.get('gender')
        teacher.date_of_birth = request.POST.get('date_of_birth')
        teacher.mobile_number = request.POST.get('mobile_number')
        teacher.joining_date = request.POST.get('joining_date')
        teacher.experience = request.POST.get('experience')
        teacher.address = request.POST.get('address')
        
        department_id = request.POST.get('department_id')
        teacher.department = Department.objects.get(id=department_id)
        teacher.save()
        return redirect('teacher_list')

    return render(request, 'teacher/edit-teacher.html', {'teacher': teacher, 'departments': departments})

# 5. Voir les détails d'un professeur — ADMIN seulement
@admin_required
def view_teacher(request, id):
    teacher = Teacher.objects.get(id=id)
    
    User = get_user_model()
    teacher_email = ""
    users = User.objects.filter(first_name=teacher.first_name, last_name=teacher.last_name, is_teacher=True)
    if users.exists():
        teacher_email = users.first().email

    return render(request, 'teacher/teacher-details.html', {
        'teacher': teacher,
        'teacher_email': teacher_email
    })