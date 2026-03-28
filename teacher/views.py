from django.shortcuts import render, redirect
from department.models import Department
from .models import Teacher

# 1. Afficher la liste des professeurs (Le "R")
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher/teachers.html', {'teachers': teachers})

def teacher_dashboard(request):
    return render(request, 'teacher/teacher-dashboard.html')

# 2. Ajouter un professeur (Le "C")
def add_teacher(request):
    if request.method == 'POST':
        # Récupération des données du formulaire
        teacher_id = request.POST.get('teacher_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        mobile_number = request.POST.get('mobile_number')
        joining_date = request.POST.get('joining_date')
        experience = request.POST.get('experience')
        address = request.POST.get('address')
        
        # L'étape clé : on récupère le vrai département grâce à l'ID envoyé par la liste déroulante
        department_id = request.POST.get('department_id')
        department = Department.objects.get(id=department_id)

        # Création et sauvegarde
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

    # Si on arrive sur la page, on charge le formulaire avec les départements disponibles
    departments = Department.objects.all()
    return render(request, 'teacher/add-teacher.html', {'departments': departments})

# 3. Supprimer un professeur (Le "D")
def delete_teacher(request, id):
    # On va chercher le prof spécifique dans la base de données
    teacher = Teacher.objects.get(id=id)
    # On le supprime
    teacher.delete()
    # On redirige vers la liste qui sera mise à jour
    return redirect('teacher_list')

# 4. Modifier un professeur
def edit_teacher(request, id):
    # On récupère le prof à modifier et tous les départements pour la liste déroulante
    teacher = Teacher.objects.get(id=id)
    departments = Department.objects.all()

    if request.method == 'POST':
        # On écrase les anciennes données avec les nouvelles du formulaire
        teacher.teacher_id = request.POST.get('teacher_id')
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.gender = request.POST.get('gender')
        teacher.date_of_birth = request.POST.get('date_of_birth')
        teacher.mobile_number = request.POST.get('mobile_number')
        teacher.joining_date = request.POST.get('joining_date')
        teacher.experience = request.POST.get('experience')
        teacher.address = request.POST.get('address')
        
        # Mise à jour du département
        department_id = request.POST.get('department_id')
        teacher.department = Department.objects.get(id=department_id)
        
        teacher.save() # On sauvegarde les modifications
        return redirect('teacher_list')

    # Si on arrive sur la page, on envoie les données actuelles du prof au HTML
    return render(request, 'teacher/edit-teacher.html', {'teacher': teacher, 'departments': departments})
# 5. Voir les détails d'un professeur
def view_teacher(request, id):
    teacher = Teacher.objects.get(id=id)
    return render(request, 'teacher/teacher-details.html', {'teacher': teacher})