from django.shortcuts import render, redirect
from department.models import Department
from .models import Teacher
from home_auth.decorators import admin_required

# 1. Liste des professeurs — ADMIN seulement
@admin_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher/teachers.html', {'teachers': teachers})

# Dashboard teacher — accessible au teacher lui-même
def teacher_dashboard(request):
    return render(request, 'teacher/teacher-dashboard.html')

# 2. Ajouter un professeur — ADMIN seulement
@admin_required
def add_teacher(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
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
        return redirect('teacher_list')

    departments = Department.objects.all()
    return render(request, 'teacher/add-teacher.html', {'departments': departments})

# 3. Supprimer un professeur — ADMIN seulement
@admin_required
def delete_teacher(request, id):
    teacher = Teacher.objects.get(id=id)
    teacher.delete()
    return redirect('teacher_list')

# 4. Modifier un professeur — ADMIN seulement
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
    return render(request, 'teacher/teacher-details.html', {'teacher': teacher})