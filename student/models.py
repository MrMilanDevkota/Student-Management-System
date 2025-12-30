from django.db import models

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    grade=models.CharField(max_length=10)
    date_of_birth = models.DateField()
    fathers_name = models.CharField(max_length=30, null=True, blank=True)
    mother_name = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, unique=True)
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True, null=True, blank=True)
    enrollment_date = models.DateField()
    image = models.ImageField(upload_to='student_images/', null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"