from django.contrib import admin
from .models import Course, Video, Test, Question

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'capacity', 'semester')
    search_fields = ('code', 'name')
    list_filter = ('department', 'semester')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'duration')
    list_filter = ('course',)
    search_fields = ('title', 'course__name')

# courses/admin.py
from django.contrib import admin
from .models import Test, Question

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'pass_mark')  # Fields to display in the admin list view
    search_fields = ('course__name', 'title')  # Fields to search in the admin panel

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('test', 'text', 'correct_option')  # Fields to display in the admin list view
    list_filter = ('test',)  # Filter questions by test
    search_fields = ('text', 'correct_option')  # Fields to search in the admin panel
  
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'date_issued')
    list_filter = ('course', 'date_issued')  # Optional filtering
    search_fields = ('student__username', 'course__name')  # Optional search capability
