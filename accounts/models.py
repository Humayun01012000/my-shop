# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.jpg'
    )
    
    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('accounts:profile')