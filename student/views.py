from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from student.models import *
from django.contrib.auth.decorators import login_required
from .decorators import role_required


# Create your views here.

def home_page(request):
    if request.user.is_authenticated:
        return redirect('index')  # If logged in, go to index
    return render(request, 'landing_page.html')



@login_required(login_url='login')
def index(request):
        # Pass user role to template for conditional rendering
    context = {
        'user_role': request.user.profile.role if hasattr(request.user, 'profile') else None
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logged out successfully.")
    return redirect('login')



@login_required(login_url='login')
@role_required('admin', 'teacher')
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

@login_required()
def read_students(request):
    students = Student.objects.all()
    return render(request, 'read_student.html', {'students': students})

@login_required(login_url='login')
def student_detail(request, student_id):
    student = Student.objects.get(id=student_id)
    return render(request, 'student_detail.html', {'student': student})

@login_required(login_url='login')
@role_required('admin', 'teacher')
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

@login_required(login_url='login')
@role_required('admin')
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        if request.POST.get('confirm'):
            student_name = f"{student.first_name} {student.last_name}"
            student.delete()
            messages.success(request, f'{student_name} has been deleted successfully.')
            return redirect('read_students')
        else:
            messages.error(request, 'Please confirm the deletion by checking the checkbox.')
    
    return render(request, 'delete_student.html', {'student': student})


