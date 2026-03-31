from django.db import models
from student.models import Student # On importe le modèle Student que tu as déjà créé

class Exam(models.Model):
    name = models.CharField(max_length=100) # Ex: "Contrôle continu 1"
    exam_date = models.DateField()
    subject = models.CharField(max_length=100) # Tu pourras lier ça à un modèle Subject plus tard
    exam_class = models.CharField(max_length=50) # Ex: "S5"

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks = models.DecimalField(max_digits=5, decimal_places=2) # Pour avoir des notes comme 15.50
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.first_name} - {self.exam.name} : {self.marks}"
