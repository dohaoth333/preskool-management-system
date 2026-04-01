from django.db import models

class TimeTable(models.Model):
    # Liste des jours de la semaine pour le menu déroulant
    DAYS_OF_WEEK = [
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'),
        ('Vendredi', 'Vendredi'),
        ('Samedi', 'Samedi'),
    ]

    teacher_name = models.CharField(max_length=100, verbose_name="Nom du Professeur")
    subject_name = models.CharField(max_length=100, verbose_name="Matière")
    class_name = models.CharField(max_length=50, verbose_name="Classe (ex: S5 - IDAI)")
    day = models.CharField(max_length=20, choices=DAYS_OF_WEEK, verbose_name="Jour")
    start_time = models.TimeField(verbose_name="Heure de début")
    end_time = models.TimeField(verbose_name="Heure de fin")

    def __str__(self):
        return f"{self.class_name} - {self.subject_name} ({self.day})"