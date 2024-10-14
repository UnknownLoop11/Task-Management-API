from django.db import models
from django.core.exceptions import ValidationError
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Validator to ensure due_date is not in the past
def validate_due_date(value):
    if value < datetime.date.today():
        raise ValidationError(f'Due date cannot be in the past. Current date is {datetime.date.today()}.')


class Task(models.Model):
    # Choices for status and priority as tuples
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Status and priority fields with choices
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    
    # Due date with custom validation
    due_date = models.DateField(null=True, validators=[validate_due_date])
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title
    
    # Example method to check if the task is overdue
    def is_overdue(self):
        """Returns True if the task's due date is past today's date."""
        if self.due_date and self.due_date < datetime.date.today():
            return True
        return False
