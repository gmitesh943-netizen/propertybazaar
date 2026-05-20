from django.db import models
from django.conf import settings
from properties.models import Property

class SiteVisit(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='site_visits')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='site_visits')
    visit_date = models.DateField()
    visit_time = models.TimeField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visit by {self.user.email} for {self.property.title}"
