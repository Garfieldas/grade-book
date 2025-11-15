from django import forms
from academics.services.lists import get_teacher_students, get_subjects_for_student
from academics.models import Semester
from django.utils import timezone

class AddGrade(forms.Form):
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            students = get_teacher_students(teacher)
            self.fields['student'].choices = [(user.id, f"{user.first_name} {user.last_name}") for user in students]
            semester = Semester.objects.filter(is_active=True).first()
            self.fields['date'].initial = timezone.now()
            self.fields['date'].widget.attrs['min'] = semester.start_date
            self.fields['date'].widget.attrs['max'] = semester.end_date
        
        student_id = self.data.get('student')
        if student_id:
            subjects = get_subjects_for_student(student_id, teacher)
            self.fields['subject'].choices = [(subject.id, f"{subject.name}") for subject in subjects]
        
    student = forms.ChoiceField(
        label='Mokinys',
        choices=[],
        widget=forms.Select(attrs={'class': 'select select-bordered'})
    )
    subject = forms.ChoiceField(
        label='Dalykas',
        choices= [],
        widget=forms.Select(attrs={'class': 'select select-bordered', })
    )
    date = forms.DateField(
        label="Semesteras",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'input'})
    )
    value = forms.DecimalField(
        label='Pažymys',
        max_digits=4,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'input input-bordered',})
    )