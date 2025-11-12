
from datetime import datetime, timedelta, time
import random
from django.db import transaction
from users.models import User
from commons.models.roles import RoleChoices
from academics.models import Schedule, SchoolClass, Subject, AcademicYear
from commons.models.days import DAYS_OF_WEEKS


def _target_days_codes():
    code_map = [code for code, _ in DAYS_OF_WEEKS]
    wanted = ["TRE", "KET", "PEN"]
    return [c for c in wanted if c in code_map]


def _time_slots(start_hour=8, lesson_minutes=45, break_minutes=15, lessons=7):
    """Return list of (start_time, end_time) tuples for lessons count."""
    slots = []
    base = datetime(2000, 1, 1, start_hour, 0)
    block = timedelta(minutes=lesson_minutes + break_minutes)
    for i in range(lessons):
        s = base + i * block
        e = s + timedelta(minutes=lesson_minutes)
        slots.append((s.time(), e.time()))
    return slots


def run(class_name="10b", lessons_per_day=7, dry_run=False):
    created = 0
    updated = 0

    days = _target_days_codes()
    slots = _time_slots(lessons=lessons_per_day)

    school_class, _ = SchoolClass.objects.get_or_create(name=class_name)

    academic_year = AcademicYear.objects.filter(is_active=True).order_by("-start_date").first()
    if not academic_year:
        academic_year = AcademicYear.objects.order_by("-start_date").first()

    subjects_qs = Subject.objects.filter(teacher__isnull=False)
    all_subjects = list(subjects_qs) if subjects_qs.exists() else list(Subject.objects.all())

    if not all_subjects:
        teacher = User.objects.filter(role=RoleChoices.TEACHER).first()
        if not teacher:
            raise RuntimeError("No Subject objects found and no teacher user exists; create at least one teacher and subject before running this script.")
        subj = Subject.objects.create(name="Demo Subject", teacher=teacher)
        all_subjects = [subj]
    with transaction.atomic():
        for day_code in days:
            for idx, (start_t, end_t) in enumerate(slots, start=1):
                subject = random.choice(all_subjects)

                defaults = {
                    "subject": subject,
                    "start_time": start_t,
                    "end_time": end_t,
                    "academic_year": academic_year,
                }
                obj, created_flag = Schedule.objects.get_or_create(
                    school_class=school_class,
                    day=day_code,
                    start_time=start_t,
                    defaults=defaults,
                )
                if created_flag:
                    created += 1
                    if not dry_run:
                        obj.subject = subject
                        obj.academic_year = academic_year
                        obj.end_time = end_t
                        obj.save()
                else:
                    updated += 1

    summary = {"created": created, "existing": updated, "class": class_name, "days": days}
    print(f"Schedule generation complete: {summary}")
    return summary


if __name__ == "__main__":
    print("This script is intended to be run via `manage.py shell`:\n  python manage.py shell -c \"from commons.scripts.schedule_script import run; run()\"\n")


