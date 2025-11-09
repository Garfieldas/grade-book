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

    def clean(self):
        super().clean()
        if self.name:
            self.name = self.name.strip().Lower()

    def save(self, *args, **kwargs):
        self.name = self.name.strip().Lower()
        super(SaveAndCleanMixin, self).save(*args, **kwargs)


    class Meta:
        abtract = True