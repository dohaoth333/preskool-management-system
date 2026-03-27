from django.db import models
from department.models import Department  # Import important !

class Teacher(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=15)
    joining_date = models.DateField()
    experience = models.CharField(max_length=50) 
    address = models.TextField()
    
    # ImageField nécessite Pillow (que tu as installé)
    teacher_image = models.ImageField(upload_to='teachers/', blank=True, null=True)
    
    # Relation : Un professeur appartient à UN département
    # on_delete=models.CASCADE signifie que si le département est supprimé, 
    # les profs associés le seront aussi (ou tu peux mettre PROTECT)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"