from django.db import models

class RoleChoices(models.TextChoices):
    STUDENT = "STUDENT", "Student"
    TEACHER = "TEACHER", "Teacher"
    PARENT  = "PARENT",  "Parent"