from django.db import models
from commons.models import UUIDMixin, TimeStampMixin, SaveAndCleanMixin
from users.models import User

class SchoolClass(UUIDMixin, TimeStampMixin, SaveAndCleanMixin):
    pass

class Subject(UUIDMixin, TimeStampMixin, SaveAndCleanMixin):
    teacher = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name="subjects",
        limit_choices_to={"role": "teacher"}
    )

class AcademicYear(UUIDMixin, SaveAndCleanMixin):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields= ["start_date", "end_date"],
                name="academic_year_uniq_date",
                violation_error_message="Academic year with this start and end date exists"
            )
        ]

    def __str__(self):
        return f"{self.start_date}/{self.end_date}"
    
class Semester(UUIDMixin, SaveAndCleanMixin):
    start_date = models.DateField()
    end_date = models.DateField()
    academic_year = models.ForeignKey(
        AcademicYear, on_delete=models.SET_NULL, null=True, related_name="semesters"
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields= ["start_date", "end_date"],
                name="semester_uniq_date",
                violation_error_message="Semester with this start and end date exists"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.academic_year})"
    
class Schedule(UUIDMixin):
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.SET_NULL, null=True, related_name="schedule"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, null=True, related_name="lessons"
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.school_class} - {self.subject} ({self.start_date})"