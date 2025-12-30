from django.contrib import admin
from django.urls import path
from student import views

urlpatterns = [
    # path('admin/', admin.site.urls),
   path('', views.index, name='index'),
    path('create_student/', views.create_student, name='create_student'),
    path('read_students/', views.read_students, name='read_students'),
    path('student_detail/<int:student_id>/', views.student_detail, name='student_detail'),
    path('update_student/<int:student_id>/', views.update_student, name='update_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),

]