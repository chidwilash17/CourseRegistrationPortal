# students/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Link to User
    department = models.CharField(max_length=50, blank=True, null=True)  # Department (optional)
    completed_courses = models.ManyToManyField('courses.Course', blank=True)  # Completed courses

    def __str__(self):
        return self.user.username