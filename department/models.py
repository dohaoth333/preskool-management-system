from django.db import models

class Department(models.Model):
    # Identifiant unique du département (ex: INF01)
    department_id = models.CharField(max_length=20, unique=True)
    # Nom du département (ex: Informatique)
    department_name = models.CharField(max_length=100)
    # Nom du chef de département
    head_of_department = models.CharField(max_length=100)
    # Date de création ou début
    start_date = models.DateField()
    # Nombre d'étudiants (optionnel, peut être mis à jour manuellement)
    no_of_students = models.IntegerField(default=0)

    def __str__(self):
        return self.department_name