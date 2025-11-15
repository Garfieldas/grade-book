from django.contrib import admin
from commons.admin import BaseAdmin
from users.models import User

@admin.register(User)
class UserAdmin(BaseAdmin):
    fieldsets = (
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Password", {"fields": ("password",)}),
        ("Status", {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
        ("Additional Info", {"fields": ("date_joined", "last_login",)}),
    )

    list_display = (
        "first_name",
        "last_name",
        "email",
        "is_active",
        "role",
        "is_mentor"
    )
    readonly_fields = ("date_joined", "last_login")

    list_filter = ("role", "is_mentor", "is_staff")
    search_fields = ("first_name", "last_name", "email")
    ordering = ('last_name', 'first_name')

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get('password')
        if password and 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

    def update(self, request, obj, form, change):
        password = form.cleaned_data.get('password')
        if password and 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        super().update(request, obj, form, change)