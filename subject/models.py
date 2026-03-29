from django.db import models
from department.models import Department
from teacher.models import Teacher


class Subject(models.Model):
    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    credits = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"
