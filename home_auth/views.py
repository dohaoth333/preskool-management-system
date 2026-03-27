from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser

def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie !")
            
            # --- LOGIQUE DE REDIRECTION SELON LE RÔLE ---
            if user.is_student:
                return redirect('student_dashboard')  # Envoie l'élève sur son dashboard
            elif user.is_teacher:
                return redirect('teacher_dashboard')  # Envoie le prof sur le sien (si tu l'as créé)
            else:
                return redirect('index')  # L'admin va sur le dashboard général
        else:
            messages.error(request, "Email ou mot de passe invalide.")
            
    return render(request, 'Home/login.html')

# --- Inscription (Register) ---
def register_user(request):
    if request.method == 'POST':
        # 1. Récupération des données du formulaire HTML
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')  # <-- NOUVEAU : On récupère le rôle choisi !

        # 2. Vérification des mots de passe
        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas !")
            return render(request, 'Home/register.html')

        # 3. Vérification si l'utilisateur existe déjà
        if CustomUser.objects.filter(username=email).exists():
            messages.error(request, "Un compte avec cet email existe déjà !")
            return render(request, 'Home/register.html')

        # 4. Préparation des rôles selon le choix du menu déroulant
        is_student = False
        is_teacher = False
        is_admin = False

        if role == 'student':
            is_student = True
        elif role == 'teacher':
            is_teacher = True
        elif role == 'admin':
            is_admin = True

        # 5. Création du nouvel utilisateur avec le bon rôle
        user = CustomUser.objects.create_user(
            username=email, 
            email=email, 
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_student=is_student,
            is_teacher=is_teacher,
            is_admin=is_admin
        )
        user.save()

        # 6. Message de succès et redirection
        messages.success(request, f"Compte {role} créé avec succès ! Vous pouvez vous connecter.")
        return redirect('login')

    # Affichage du formulaire vide (méthode GET)
    return render(request, 'Home/register.html')

# --- Déconnexion (Logout) ---
def logout_user(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')