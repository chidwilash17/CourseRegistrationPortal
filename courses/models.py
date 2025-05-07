# courses/models.py
from django.db import models
from students.models import Student

# Course Model
# courses/models.py
from django.db import models

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)  # Course code
    name = models.CharField(max_length=100)  # Course name
    description = models.TextField()  # Course description
    department = models.CharField(max_length=50)  # Department
    credits = models.IntegerField()  # Number of credits
    capacity = models.IntegerField()  # Maximum number of students
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)  # Prerequisite courses
    semester = models.CharField(max_length=20, choices=[('1', '1st Semester'), ('2', '2nd Semester')])  # Semester
    instructor = models.CharField(max_length=100)  # Instructor name

    def __str__(self):
        return f"{self.code} - {self.name}"
# Test Model
class Test(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='test')
    title = models.CharField(max_length=100)
    pass_mark = models.IntegerField(help_text="Minimum marks required to pass")

    def __str__(self):
        return f"{self.course.name} - {self.title}"

# Question Model
class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.test.title} - {self.text[:50]}"

# Certificate Model
class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE) 
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField(default=0) 
    date_issued = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name}"

# Registration Model
class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link to the Student model
    course = models.ForeignKey('Course', on_delete=models.CASCADE)  # Link to the Course model
    date_registered = models.DateTimeField(auto_now_add=True)  # Date of registration
    status = models.CharField(
        max_length=20,
        choices=[('registered', 'Registered'), ('waitlisted', 'Waitlisted')],
        default='registered'
    )  # Registration status

    def __str__(self):
        return f"{self.student.user.username} - {self.course.code}"

# Video Model
class Video(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    duration = models.PositiveIntegerField()  # Duration in minutes
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.title
class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=200)
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.question.text[:50]}"
    from django.db import models
from django.contrib.auth.models import User
class Comment(models.Model):
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.text[:50]}'