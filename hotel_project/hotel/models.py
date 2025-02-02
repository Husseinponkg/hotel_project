from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    culture_choice = models.CharField(max_length=20, choices=[
        ('African', 'African'),
        ('American', 'American'),
        ('European', 'European'),
        ('Arabic', 'Arabic'),
    ])
    origin = models.CharField(max_length=20, choices=[
        ('african', 'Africa'),
        ('american', 'America'),
        ('european', 'Europe'),
        ('arabic', 'Arab'),
    ], default='african')  # Provide a default value

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'hotel'