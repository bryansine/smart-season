from datetime import date
from django.db import models
from django.conf import settings
from django.utils import timezone

class Field(models.Model):
    STAGE_CHOICES = [
        ('planted', 'Planted'),
        ('growing', 'Growing'),
        ('ready', 'Ready to Harvest'),
        ('harvested', 'Harvested'),
    ]

    name = models.CharField(max_length=200)
    crop_type = models.CharField(max_length=100)
    planting_date = models.DateField()
    current_stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='planted')

    assigned_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assigned_fields',
        limit_choices_to={'is_field_agent': True}
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, related_name='created_fields'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def computed_status(self):
        if self.current_stage == 'harvested':
            return "Completed"

        today = date.today()
        days_since_planting = (today - self.planting_date).days
        
        last_update = self.updates.first()
        
        if last_update:
            days_since_update = (timezone.now() - last_update.created_at).days
        else:
            days_since_update = days_since_planting

        if days_since_planting > 90 and days_since_update > 14:
            return "At Risk"
        if self.current_stage == 'planted' and days_since_planting > 30:
            return "At Risk"

        return "Active"

    @property
    def status_badge_class(self):
        mapping = {
            "Active": "success",
            "At Risk": "danger",
            "Completed": "secondary"
        }
        return mapping.get(self.computed_status, "info")

    def __str__(self):
        return f"{self.name} ({self.crop_type})"

    class Meta:
        ordering = ['-created_at']

class FieldUpdate(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='updates')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    stage = models.CharField(max_length=20, choices=Field.STAGE_CHOICES)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']