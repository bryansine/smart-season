from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_coordinator = models.BooleanField(
        default=False,
        help_text='Admin role — can view all fields and monitor all agents.'
    )
    is_field_agent = models.BooleanField(
        default=False,
        help_text='Field agent role — can only see and update assigned fields.'
    )


    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @property
    def role_display(self):
        if self.is_coordinator: return 'Coordinator'
        if self.is_field_agent: return 'Field Agent'
        return 'Customer'