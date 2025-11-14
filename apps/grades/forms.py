from django import forms
from academics.services.lists import get_teacher_students
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

            self.fields['semester'].initial = f"{semester.name}"
            self.fields['semester'].widget.attrs['readonly'] = True

            self.fields['date'].initial = timezone.now()
            self.fields['date'].widget.attrs['min'] = semester.start_date
            self.fields['date'].widget.attrs['max'] = semester.end_date
        
        
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
    semester = forms.DateField(
        label="Semesteras",
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'input'})
    )
    date = forms.DateField(
        label="Semesteras",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'input'})
    )
    value = forms.DecimalField(
        label='Pažymys',
        max_digits=4,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'input input-bordered', 'step': '0.01'})
    )