from django.db import models
from django.utils import timezone


class MyModel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    upload = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    # class Meta:
    #     ordering = ['updated_at']