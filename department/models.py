from django.db import models

class Department(models.Model):
    department_id = models.CharField(max_length=50, unique=True)
    department_name = models.CharField(max_length=100)
    head_of_department = models.CharField(max_length=100)
    start_date = models.DateField()
    no_of_students = models.IntegerField(default=0)

    def __str__(self):
        return self.department_name