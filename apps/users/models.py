from django.db import models
from django.contrib.auth.models import AbstractUser
from commons.models.roles import RoleChoices
from users.managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=RoleChoices.choices)
    is_mentor = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=["first_name", "last_name"]),
            models.Index(fields=["role"]),
        ]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

    def clean(self):
        super().clean()
        if self.email:
            self.email = self.email.strip().lower()

    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"