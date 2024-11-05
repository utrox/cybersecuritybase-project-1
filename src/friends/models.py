from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=128)
    friends = models.ManyToManyField('self', blank=True)

    # createsuperuser command requires these fields
    REQUIRED_FIELDS = ['address', 'phone_number', 'date_of_birth']


class Secret(models.Model):
    # Shhhhhhhhh.....
    secret_data = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
