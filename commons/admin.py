from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20
    show_full_result_count = False
    warn_unsaved_form = True
    search_help_text = "Type to search"