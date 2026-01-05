from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from student.models import *
from django.contrib.auth.decorators import login_required


# Create your views here.

def home_page(request):
    if request.user.is_authenticated:
        return redirect('index')  # If logged in, go to index
    return render(request, 'landing_page.html')



def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not all([username, email, first_name, last_name, password1, password2]):
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
        except Exception as e:
                print(f"Error creating user: {e}")
                messages.error(request, "Something went wrong while creating your account. Please try again.")
                return redirect('register')

        login(request, user)
        messages.success(request, "Registration successful! 🎉")
        return redirect('index')

    return render(request, 'register.html')



def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')


@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logged out successfully.")
    return redirect('login')



@login_required(login_url='login')
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


