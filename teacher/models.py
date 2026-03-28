from django.db import models
from department.models import Department # Très important !

class Teacher(models.Model):
    teacher_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=20)
    joining_date = models.DateField()
    experience = models.CharField(max_length=50)
    address = models.TextField()
    
    # C'est ici qu'on relie le prof à son département
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    # On peut laisser l'image en commentaire pour l'instant pour simplifier le CRUD
    # image = models.ImageField(upload_to='teachers/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"