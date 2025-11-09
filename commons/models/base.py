from django.db import models
import uuid

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class SaveAndCleanMixin(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def clean(self):
        super().clean()
        if self.name:
            self.name = self.name.strip().lower()

    def save(self, *args, **kwargs):
        self.name = self.name.strip().lower()
        super(SaveAndCleanMixin, self).save(*args, **kwargs)


    class Meta:
        abstract = True