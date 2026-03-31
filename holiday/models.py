from django.db import models


class Holiday(models.Model):
    HOLIDAY_TYPE_CHOICES = [
        ('national', 'Jour Férié National'),
        ('religious', 'Fête Religieuse'),
        ('school', 'Vacances Scolaires'),
        ('other', 'Autre'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nom du jour férié")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")
    holiday_type = models.CharField(
        max_length=20,
        choices=HOLIDAY_TYPE_CHOICES,
        default='national',
        verbose_name="Type"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']
        verbose_name = "Jour Férié"
        verbose_name_plural = "Jours Fériés"

    def __str__(self):
        return f"{self.name} ({self.start_date})"

    @property
    def duration(self):
        """Retourne le nombre de jours du congé."""
        return (self.end_date - self.start_date).days + 1
