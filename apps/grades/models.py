from django.db import models
from users.models import User
from academics.models import Subject, Semester
from commons.models import UUIDMixin, TimeStampMixin, RoleChoices
from django.core.validators import MinValueValidator, MaxValueValidator

class Mark(UUIDMixin, TimeStampMixin):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="marks",
        limit_choices_to={"role": RoleChoices.STUDENT},
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, null=True, related_name="marks"
    )
    semester = models.ForeignKey(
        Semester, on_delete=models.SET_NULL, null=True, related_name="marks"
    )
    mark_date = models.DateField()

    value = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(2), MaxValueValidator(10)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "subject", "semester", "mark_date"],
                name="unique_current_mark",
                violation_error_message="Student already has mark for this day in this subject"
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.value}"
