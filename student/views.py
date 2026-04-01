from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student, Parent
from home_auth.decorators import admin_required, admin_or_teacher_required

# --- Affiche le Dashboard  
@login_required(login_url='login')
def student_dashboard(request):
    return render(request, 'students/student-dashboard.html')

# --- Affiche la liste des étudiants --- ADMIN et TEACHER
@admin_or_teacher_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/students.html', {'student_list': students})

# --- Gère l'ajout d'un étudiant --- ADMIN et TEACHER
@admin_or_teacher_required
def add_student(request):
    if request.method == 'POST':
        # 1. RÃ©cupÃ©rer les donnÃ©es de l'Ã©tudiant
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')

        # 2. RÃ©cupÃ©rer les donnÃ©es du parent
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        # 3. CrÃ©er et sauvegarder le parent
        parent = Parent.objects.create(
            father_name=father_name,
            father_occupation=father_occupation,
            father_mobile=father_mobile,
            father_email=father_email,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            mother_mobile=mother_mobile,
            mother_email=mother_email,
            present_address=present_address,
            permanent_address=permanent_address
        )

        # 4. CrÃ©er l'Ã©tudiant liÃ© au parent
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            student_id=student_id,
            gender=gender,
            date_of_birth=date_of_birth,
            student_class=student_class,
            joining_date=joining_date,
            mobile_number=mobile_number,
            admission_number=admission_number,
            section=section,
            student_image=student_image,
            parent=parent
        )

        messages.success(request, 'Student added Successfully')
        return redirect('student_list')

    return render(request, 'students/add-student.html')

# --- Affiche les détails d'un étudiant --- ADMIN et TEACHER
@admin_or_teacher_required
def view_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student-details.html', {'student': student})

# --- Formulaire et logique de modification --- ADMIN et TEACHER
# --- Formulaire et logique de modification --- ADMIN et TEACHER
@admin_or_teacher_required
def edit_student(request, student_id):
    # On récupère l'étudiant via son matricule (student_id) et non plus par son ID technique (pk)
    student = get_object_or_404(Student, student_id=student_id)

    if request.method == 'POST':
        # On met à jour les champs de l'étudiant
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.gender = request.POST.get('gender')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.student_class = request.POST.get('student_class')
        student.mobile_number = request.POST.get('mobile_number')

        # Gestion de l'image (seulement si une nouvelle image est téléchargée)
        if request.FILES.get('student_image'):
            student.student_image = request.FILES.get('student_image')

        student.save()
        messages.success(request, 'Student updated successfully!')
        return redirect('student_list')

    return render(request, 'students/edit-student.html', {'student': student})

# --- Supprime un étudiant --- ADMIN et TEACHER
@admin_or_teacher_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('student_list')