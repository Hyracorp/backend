from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(f"{email} is not a valid email address")

    def create_user(self, email, password,first_name, last_name, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        self.email_validator(email)
        
        if not first_name:
            raise ValueError("The first name must be set")
        if not last_name:
            raise ValueError("The last name must be set")
        user = self.model(email=email, first_name=first_name, last_name=last_name **extra_fields)
        if password:
            user.set_password(password)  # Hash the password
        else:
            user.set_unusable_password()  # Ensure a password is set
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password,first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        user= self.create_user(email, password,first_name, last_name, **extra_fields)
        user.save(using=self._db)
        return user