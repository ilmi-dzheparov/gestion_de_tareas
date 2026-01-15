from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Securely hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    # Use Boolean flags to allow a user to potentially be both
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    # Your original fields
    dni = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    birthdate = models.DateField(null=True, blank=True)
    group = models.ForeignKey(
        'taskapp.Group',
        on_delete=models.PROTECT,
        related_name='users',
        null=True, # Optional: helps if you create a superuser without a department
        blank=True
    )

    # Required infrastructure for AbstractBaseUser
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"   # Students will login using email
    REQUIRED_FIELDS = ["name"] # Fields prompted for during 'createsuperuser'

    def __str__(self):
        return f"{self.last_name}, {self.name}"
