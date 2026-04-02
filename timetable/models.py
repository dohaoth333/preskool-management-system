from django.db import models
from home_auth.models import CustomUser

class TimeTable(models.Model):
    # List of days of the week for the dropdown
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    teacher_name = models.CharField(max_length=100, verbose_name="Teacher Name")
    subject_name = models.CharField(max_length=100, verbose_name="Subject")
    class_name = models.CharField(max_length=50, verbose_name="Class (e.g. S5 - IDAI)")
    day = models.CharField(max_length=20, choices=DAYS_OF_WEEK, verbose_name="Day")
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")

    def __str__(self):
        return f"{self.class_name} - {self.subject_name} ({self.day})"

class ScheduleProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='proposals')
    teacher_name = models.CharField(max_length=100) # For display consistency
    subject_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    day = models.CharField(max_length=20, choices=TimeTable.DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposal by {self.teacher.username} for {self.class_name} - {self.subject_name}"