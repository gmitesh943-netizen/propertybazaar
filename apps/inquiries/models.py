from django.db import models
from django.conf import settings
from properties.models import Property

class Inquiry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inquiries', null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry for {self.property.title} by {self.name}"
