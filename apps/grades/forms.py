from django import forms
from academics.services.lists import get_teacher_students, get_subjects_for_student
from academics.models import Semester, Subject
from grades.models import Mark
from django.utils import timezone
from users.models import User
from django.urls import reverse

class SubjectChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class AddGrade(forms.Form):        
    student = forms.ModelChoiceField(
        label='Mokinys',
        queryset=User.objects.none(),
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )
    subject = SubjectChoiceField(
        label='Dalykas',
        queryset=Subject.objects.none(),
        widget=forms.Select(attrs={'class': 'select select-bordered w-full', })
    )
    date = forms.DateField(
        label="Data",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'input'})
    )
    value = forms.DecimalField(
        label='Pažymys',
        max_digits=4,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'input input-bordered',})
    )
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['student'].queryset = get_teacher_students(teacher)
            self.fields['student'].widget.attrs.update({
            "hx-get": reverse("get_subjects_for_student"),
            "hx-trigger": "change",
            "hx-target": "#id_subject",
            "hx-swap": "innerHTML",
            "hx-vals": "js:{student_id: event.target.value}",
            })
            semester = Semester.objects.filter(is_active=True).first()
            today = timezone.now().date()
            self.fields['date'].initial = today
            self.fields['date'].widget.attrs['min'] = semester.start_date
            self.fields['date'].widget.attrs['max'] = today
        
        student = self.data.get('student')
        if student:
            self.fields['subject'].queryset = get_subjects_for_student(student, teacher)

    def clean(self):
        cleaned = super().clean()

        student = cleaned.get("student")
        subject = cleaned.get("subject")
        date    = cleaned.get("date")
        value   = cleaned.get("value")
        today = timezone.now().date()

        semester = Semester.objects.filter(is_active=True).first()

        if value is not None and not (2 <= value <= 10):
            self.add_error("value", "Pažymys turi būti tarp 2 ir 10.")

        if student is None:
            self.add_error("student", "Pasirinkite mokinį.")

        if subject is None:
            self.add_error("subject", "Pasirinkite dalyką.")

        if date is None:
            self.add_error("date", "Data privaloma.")
        elif semester and not (semester.start_date <= date <= today):
            self.add_error("date", f"Data turi būti tarp {semester.start_date} ir {today}.")

        if student and subject and date and semester:
            if Mark.objects.filter(
            student=student,
            subject=subject,
            mark_date=date,
            semester=semester
            ).exists():
                self.add_error("date", "Mokinys jau turi pažymį šiai datai.")

        return cleaned

class GradeModal(forms.ModelForm):
    subject = SubjectChoiceField(
        label='Dalykas',
        queryset=Subject.objects.none(),
        widget=forms.Select(attrs={'class': 'select select-bordered w-full', })
    )
    date = forms.DateField(
        label="Data",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'input'})
    )
    value = forms.DecimalField(
        label='Pažymys',
        max_digits=4,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'input input-bordered',})
    )
    class Meta:
        model = Mark
        fields = ['subject', 'date', 'value']

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        self.student_id = kwargs.pop('student_id', None)
        super().__init__(*args, **kwargs)
        if teacher:
            semester = Semester.objects.filter(is_active=True).first()
            today = timezone.now().date()
            self.fields['date'].initial = today
            self.fields['date'].widget.attrs['min'] = semester.start_date
            self.fields['date'].widget.attrs['max'] = today
        
        student = User.objects.get(pk=self.student_id)
        if student:
            self.fields['subject'].queryset = get_subjects_for_student(student, teacher)

    def clean(self):
        cleaned = super().clean()

        subject = cleaned.get("subject")
        date    = cleaned.get("date")
        value   = cleaned.get("value")
        today = timezone.now().date()

        semester = Semester.objects.filter(is_active=True).first()
        student = User.objects.get(pk=self.student_id)

        if value is not None and not (2 <= value <= 10):
            self.add_error("value", "Pažymys turi būti tarp 2 ir 10.")

        if subject is None:
            self.add_error("subject", "Pasirinkite dalyką.")

        if date is None:
            self.add_error("date", "Data privaloma.")
        elif semester and not (semester.start_date <= date <= today):
            self.add_error("date", f"Data turi būti tarp {semester.start_date} ir {today}.")

        if student and subject and date and semester:
            if Mark.objects.filter(
            student=student,
            subject=subject,
            mark_date=date,
            semester=semester
            ).exists():
                self.add_error("date", "Mokinys jau turi pažymį šiai datai.")

        return cleaned