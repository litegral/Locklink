from django.db import models

# Create your models here.

class URL(models.Model):
    original_url = models.TextField()
    short_code = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.original_url
