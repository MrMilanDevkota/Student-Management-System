from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Student)

from django.contrib import admin
from .models import Student, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']