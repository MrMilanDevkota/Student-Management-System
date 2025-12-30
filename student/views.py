from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from student.models import *


# Create your views here.
def index(request):
    return render(request, 'index.html')

def create_student(request):
    if request.method == 'POST':
        # Handle form submission logic here
        data=request.POST
        file_=request.FILES

        Student.objects.create(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            grade=data.get('grade'),
            date_of_birth=data.get('date_of_birth'),
            fathers_name=data.get('fathers_name'),
            mother_name=data.get('mother_name'),
            address=data.get('address'),
            phone_number=data.get('phone_number'),
            gender=data.get('gender'),
            email=data.get('email'),
            enrollment_date=data.get('enrollment_date'),
            image=file_.get('image')
        )

    return render(request, 'create_student.html')

def read_students(request):
    students = Student.objects.all()
    return render(request, 'read_student.html', {'students': students})

def student_detail(request, student_id):
    student = Student.objects.get(id=student_id)
    return render(request, 'student_detail.html', {'student': student})

def update_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.grade = request.POST.get('grade')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.fathers_name = request.POST.get('fathers_name')
        student.mother_name = request.POST.get('mother_name')
        student.address = request.POST.get('address')
        student.phone_number = request.POST.get('phone_number')
        student.gender = request.POST.get('gender')
        student.email = request.POST.get('email')
        student.enrollment_date = request.POST.get('enrollment_date')
        
        if request.FILES.get('image'):
            student.image = request.FILES.get('image')
        
        student.save()
        messages.success(request, 'Student updated successfully!')
        return redirect('student_detail', student_id=student.id)
    
    return render(request, 'update_student.html', {'student': student})

def delete_student(request):
    return render(request, 'delete_student.html')

