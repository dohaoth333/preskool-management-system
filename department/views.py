from django.shortcuts import render, redirect
from .models import Department
from home_auth.decorators import admin_required

# 1. Liste des départements — ADMIN seulement
@admin_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department/departments.html', {'departments': departments})

# 2. Ajouter un département — ADMIN seulement
@admin_required
def add_department(request):
    if request.method == 'POST':
        department_id = request.POST.get('department_id')
        department_name = request.POST.get('department_name')
        head_of_department = request.POST.get('head_of_department')
        start_date = request.POST.get('start_date')
        no_of_students = request.POST.get('no_of_students')

        department = Department(
            department_id=department_id,
            department_name=department_name,
            head_of_department=head_of_department,
            start_date=start_date,
            no_of_students=no_of_students
        )
        department.save()
        return redirect('department_list')

    return render(request, 'department/add-department.html')

# 3. Modifier un département — ADMIN seulement
@admin_required
def edit_department(request, id):
    department = Department.objects.get(id=id)

    if request.method == 'POST':
        department.department_id = request.POST.get('department_id')
        department.department_name = request.POST.get('department_name')
        department.head_of_department = request.POST.get('head_of_department')
        department.start_date = request.POST.get('start_date')
        department.no_of_students = request.POST.get('no_of_students')
        department.save()
        return redirect('department_list')

    return render(request, 'department/edit-department.html', {'department': department})

# 4. Supprimer un département — ADMIN seulement
@admin_required
def delete_department(request, id):
    department = Department.objects.get(id=id)
    department.delete()
    return redirect('department_list')
