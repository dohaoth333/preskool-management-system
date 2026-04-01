from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required # Import obligatoire pour la sécurité
from .models import Exam, Result
from student.models import Student

@login_required(login_url='login') # Force l'utilisateur à être connecté
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exams/exam-list.html', {'exams': exams})

@login_required(login_url='login')
def add_exam(request):
    # --- SÉCURITÉ : Bloquer si l'utilisateur est un étudiant ---
    if getattr(request.user, 'is_student', False):
        messages.error(request, "Accès refusé : les étudiants ne peuvent pas ajouter d'examen.")
        return redirect('exam_list')

    if request.method == 'POST':
        name = request.POST.get('name')
        exam_date = request.POST.get('exam_date')
        subject = request.POST.get('subject')
        exam_class = request.POST.get('exam_class')

        Exam.objects.create(
            name=name,
            exam_date=exam_date,
            subject=subject,
            exam_class=exam_class
        )
        messages.success(request, 'Examen ajouté avec succès !')
        return redirect('exam_list')
        
    return render(request, 'exams/add-exam.html')

@login_required(login_url='login')
def add_result(request):
    # --- SÉCURITÉ : Bloquer si l'utilisateur est un étudiant ---
    if getattr(request.user, 'is_student', False):
        messages.error(request, "Accès refusé : vous ne pouvez pas modifier les notes.")
        return redirect('exam_list')

    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        student_id = request.POST.get('student_id')
        marks = request.POST.get('marks')
        
        # Récupération des instances d'Exam et de Student
        exam = Exam.objects.get(id=exam_id)
        student = Student.objects.get(id=student_id)

        Result.objects.create(
            exam=exam,
            student=student,
            marks=marks
        )
        messages.success(request, 'Note ajoutée avec succès !')
        # Rediriger vers la liste des résultats plutôt que les examens
        return redirect('result_list') 

    # Pour afficher les listes déroulantes dans le formulaire
    exams = Exam.objects.all()
    students = Student.objects.all()
    return render(request, 'exams/add-result.html', {'exams': exams, 'students': students})

@login_required(login_url='login')
def result_list(request):
    # Cette vue récupère toutes les notes de la base de données
    results = Result.objects.all()
    return render(request, 'exams/result-list.html', {'results': results})

@login_required(login_url='login')
def my_results(request):
    # 1. On vérifie que c'est bien un étudiant qui essaie d'accéder à cette page
    if not getattr(request.user, 'is_student', False):
        messages.error(request, "Cette page est réservée aux étudiants.")
        return redirect('dashboard')

    # 2. On cherche la fiche "Student" qui correspond à l'utilisateur connecté
    try:
        # On fait la correspondance avec le prénom et le nom
        student_profile = Student.objects.get(
            first_name=request.user.first_name, 
            last_name=request.user.last_name
        )
        
        # 3. On filtre les résultats : on ne prend QUE les notes de CET étudiant
        mes_notes = Result.objects.filter(student=student_profile)
        
    except Student.DoesNotExist:
        # Si le compte utilisateur n'a pas encore de fiche étudiant correspondante
        mes_notes = []
        messages.warning(request, "Votre profil étudiant n'a pas été trouvé. Contactez l'administration.")

    return render(request, 'exams/my-results.html', {'mes_notes': mes_notes})

@login_required(login_url='login')
def edit_exam(request, exam_id):
    # Sécurité : Bloquer les étudiants
    if getattr(request.user, 'is_student', False):
        messages.error(request, "Accès refusé.")
        return redirect('exam_list')

    # On récupère l'examen spécifique depuis la base de données
    exam = Exam.objects.get(id=exam_id)

    if request.method == 'POST':
        # On met à jour les informations
        exam.name = request.POST.get('name')
        exam.exam_date = request.POST.get('exam_date')
        exam.subject = request.POST.get('subject')
        exam.exam_class = request.POST.get('exam_class')
        exam.save() # On sauvegarde les modifications
        
        messages.success(request, 'Examen modifié avec succès !')
        return redirect('exam_list')

    return render(request, 'exams/edit-exam.html', {'exam': exam})

@login_required(login_url='login')
def delete_exam(request, exam_id):
    # Sécurité : Bloquer les étudiants
    if getattr(request.user, 'is_student', False):
        messages.error(request, "Accès refusé.")
        return redirect('exam_list')

    # On récupère l'examen et on le supprime
    exam = Exam.objects.get(id=exam_id)
    exam.delete()
    
    messages.success(request, 'Examen supprimé avec succès !')
    return redirect('exam_list')