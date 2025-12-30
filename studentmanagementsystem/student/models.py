from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=100)
    joined_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} ({self.roll_number})"
    
    