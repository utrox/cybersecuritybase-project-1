from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self, login, email, password, date_of_birth, phone_number, is_staff, is_admin, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        now = timezone.now()
        email = self.normalize_email(email)

        user = self.model(
            login=login,
            email=email,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            is_staff=is_staff,
            is_active=True,
            is_admin=is_admin,
            last_login=now,
            date_joined=now, 
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, login, email, password, date_of_birth, phone_number, **extra_fields):
        user = self._create_user(login, email, password, False, False, **extra_fields)
        user.save(using=self._db)
        
        return user


    def create_superuser(self, login, email, password, date_of_birth, phone_number, **extra_fields):
        user=self._create_user(login, email, password, True, True, **extra_fields)

        return user
