from django.shortcuts import render

def student_grades(request):
    return render(request, "grades/student_grades.html")

def newest_grades(request):
    return render(request, "grades/newest_grades.html")
