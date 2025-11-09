from django.contrib import admin
from commons.admin import BaseAdmin
from academics.models import SchoolClass, Subject, AcademicYear, Semester, Schedule

@admin.register(SchoolClass)
class SchoolClassAdmin(BaseAdmin):
    pass

@admin.register(Subject)
class SubjectAdmin(BaseAdmin):
    pass
@admin.register(AcademicYear)
class AcademicYearAdmin(BaseAdmin):
    pass
@admin.register(Semester)
class SemesterAdmin(BaseAdmin):
    pass
@admin.register(Schedule)
class ScheduleAdmin(BaseAdmin):
    pass
