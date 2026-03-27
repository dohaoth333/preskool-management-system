from django.db import models

# 1. Le modèle pour les Départements
class Department(models.Model):
    department_id = models.CharField(max_length=20, unique=True)
    department_name = models.CharField(max_length=100) # Ex: Informatique
    head_of_department = models.CharField(max_length=100)
    start_date = models.DateField()
    no_of_students = models.IntegerField(default=0)

    def __str__(self):
        return self.department_name

# 2. Le modèle pour les Professeurs
class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=15)
    joining_date = models.DateField()
    experience = models.CharField(max_length=50) # Ex: "5 Years"
    address = models.TextField()
    teacher_image = models.ImageField(upload_to='teachers/', blank=True)
    
    # La relation clé : Chaque prof est lié à un département
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"
