from django.shortcuts import render, redirect
from .models import Department

# 1. La fonction pour afficher la liste (le "R" de CRUD)
def department_list(request):
    # On récupère tous les départements dans la base de données
    departments = Department.objects.all()
    # On les envoie au fichier HTML
    return render(request, 'department/departments.html', {'departments': departments})

# 2. La fonction pour ajouter un département (le "C" de CRUD)
def add_department(request):
    if request.method == 'POST':
        # Si l'utilisateur clique sur Submit, on récupère les données du formulaire
        department_id = request.POST.get('department_id')
        department_name = request.POST.get('department_name')
        head_of_department = request.POST.get('head_of_department')
        start_date = request.POST.get('start_date')
        no_of_students = request.POST.get('no_of_students')

        # On crée le département dans la base de données
        department = Department(
            department_id=department_id,
            department_name=department_name,
            head_of_department=head_of_department,
            start_date=start_date,
            no_of_students=no_of_students
        )
        department.save()
        
        # On redirige vers la liste une fois que c'est sauvegardé
        return redirect('department_list')
        
    # Si c'est juste un affichage normal de la page, on charge le HTML vide
    return render(request, 'department/add-department.html')

# 3. Modifier un département (Le "U" de Update)
def edit_department(request, id):
    # On récupère le département spécifique
    department = Department.objects.get(id=id)

    if request.method == 'POST':
        # On écrase les anciennes données avec les nouvelles du formulaire
        department.department_id = request.POST.get('department_id')
        department.department_name = request.POST.get('department_name')
        department.head_of_department = request.POST.get('head_of_department')
        department.start_date = request.POST.get('start_date')
        department.no_of_students = request.POST.get('no_of_students')
        
        department.save() # On sauvegarde !
        return redirect('department_list')

    # Si c'est juste un affichage, on envoie les infos du département au HTML
    return render(request, 'department/edit-department.html', {'department': department})

# 4. Supprimer un département (Le "D" de Delete)
def delete_department(request, id):
    department = Department.objects.get(id=id)
    department.delete()
    return redirect('department_list')
