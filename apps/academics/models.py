from django.db import models
from commons.models import UUIDMixin, TimeStampMixin, SaveAndCleanMixin, RoleChoices
from users.models import User

class SchoolClass(UUIDMixin, TimeStampMixin, SaveAndCleanMixin):
    def __str__(self):
        return f"{self.name}"
    
class StudentClass(UUIDMixin, TimeStampMixin):
    student = models.OneToOneField(User,
            on_delete=models.CASCADE, related_name="student_class",
            limit_choices_to={"role": RoleChoices.STUDENT}
            )
    school_class = models.ForeignKey(SchoolClass,
            on_delete=models.SET_NULL, null=True, related_name="student")
    
    def __str__(self):
        return f"{self.student} - {self.school_class}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["student", "school_class"],
                name="unique_student_class",
                violation_error_message="student is already assigned to this class!"
            )
        ]

class Subject(UUIDMixin, TimeStampMixin, SaveAndCleanMixin):
    teacher = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name="subjects",
        limit_choices_to={"role": RoleChoices.TEACHER}
    )

    def __str__(self):
        return f"{self.name} - {self.teacher}"

class AcademicYear(UUIDMixin, SaveAndCleanMixin):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

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
    is_active = models.BooleanField(default=True)
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
    DAYS_OF_WEEKS = (
        ("PIR", "Pirmadienis"),
        ("AN", "Antradienis"),
        ("TRE", "Trečiadienis"),
        ("KET", "Ketvirtadienis"),
        ("PEN", "Penktadienis"),

    )
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.SET_NULL, null=True, related_name="schedule"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, null=True, related_name="lessons"
    )
    academic_year = models.ForeignKey(
        AcademicYear, on_delete=models.SET_NULL, null=True, related_name="schedule"
    )
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEKS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.school_class} - {self.subject} ({self.day})"