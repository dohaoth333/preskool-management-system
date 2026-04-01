from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Configuration optionnelle pour bien afficher les colonnes dans l'admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_student', 'is_teacher', 'is_admin']
    # On ajoute vos champs personnalisés pour qu'ils soient modifiables
    fieldsets = UserAdmin.fieldsets + (
        ('Roles', {'fields': ('is_student', 'is_teacher', 'is_admin')}),
    )

# On enregistre le modèle avec sa configuration
admin.site.register(CustomUser, CustomUserAdmin)