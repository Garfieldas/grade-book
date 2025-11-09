from django.contrib import admin
from commons.admin import BaseAdmin
from grades.models import Mark

@admin.register(Mark)
class MarkAdmin(BaseAdmin):
    pass