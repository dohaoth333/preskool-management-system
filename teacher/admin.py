from django.contrib import admin
from .models import Department, Teacher

# Enregistrement du modèle Department
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'department_name', 'head_of_department', 'no_of_students')
    search_fields = ('department_id', 'department_name')

# Enregistrement du modèle Teacher
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'teacher_id', 'department', 'mobile_number')
    search_fields = ('first_name', 'last_name', 'teacher_id')
    list_filter = ('gender', 'department')