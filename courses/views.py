# courses/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Course, Registration,Video, Test, Certificate, Question
from students.models import Student
from .forms import VideoUploadForm
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import SemesterForm
from .models import Course
from django.urls import reverse

# Register View

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        semester = request.POST.get('semester')  # Get the selected semester

        # Validate passwords
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Log the user in
        login(request, user)

        # Save the selected semester in the session
        request.session['semester'] = semester

        # Redirect to the course search page
        return redirect('login')
    else:
        return render(request, 'register.html')
# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')  # Redirect to home page after login
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# View to display a list of courses
def course_list(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if not authenticated

    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

# View to search for courses
from django.shortcuts import render
from django.db.models import Q
from .models import Course
from .forms import SearchForm

def course_search(request):
    # Get the selected semester from the session
    semester = request.session.get('semester')

    # Get the search query from the request
    query = request.GET.get('query', '')

    # Start with all courses or filter by semester if selected
    if semester:
        courses = Course.objects.filter(semester=semester)
    else:
        courses = Course.objects.all()

    # Apply search filtering if a query is provided
    if query:
        courses = courses.filter(
            Q(name__icontains=query) | Q(code__icontains=query) | Q(description__icontains=query)
        )

    # Pass the filtered courses, search form, and query to the template
    context = {
        'courses': courses,
        'form': SearchForm(),
        'query': query,
        'semester': semester,
    }
    return render(request, 'course_search.html', context)


# View to display details of a specific course
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = course.videos.all()
    return render(request, 'course_detail.html', {'course': course, 'videos': videos})

# View to register for a course
# courses/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Course, Registration
from students.models import Student


def register_course(request, course_id):
    # Get the course or return a 404 error if it doesn't exist
    course = get_object_or_404(Course, id=course_id)

    # Check if the user is logged in
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to register for a course.')
        return redirect('login')  # Redirect to the login page

    try:
        # Get the student profile for the logged-in user
        student = request.user.student
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found. Please contact the administrator.')
        

    # Check if the student meets the prerequisites
   
        

    # Check if the course is full
    if Registration.objects.filter(course=course, status='registered').count() >= course.capacity:
        # Add the student to the waitlist
        Registration.objects.create(student=student, course=course, status='waitlisted')
        messages.warning(request, 'Course is full. You have been added to the waitlist.')
    else:
        # Register the student for the course
        Registration.objects.create(student=student, course=course, status='registered')
        messages.success(request, 'Course registration successful.')

    # Redirect back to the course search page
    return redirect('course_search')
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Registration

def unregister_course(request, registration_id):
    student = Student.objects.get(user=request.user)  # Fetch the Student instance
    registration = Registration.objects.get(id=registration_id, student=student)
    registration.delete()
    return redirect('dashboard')

# View to take a test for a course
def take_test(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    test = course.test
    questions = test.questions.all()
    return render(request, 'take_test.html', {'course': course, 'test': test, 'questions': questions})

# View to submit a test and evaluate results
def submit_test(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        test = course.test
        questions = test.questions.all()
        score = 0

        # Evaluate answers
        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option == question.correct_option:
                score += 1

        # Check if the student passed
        if score >= test.pass_mark:
            Certificate.objects.create(student=request.user.student, course=course)
            certificate = Certificate(course=course, student=request.user.student)
            certificate.save()
            messages.success(request, 'Congratulations! You passed the test and earned a certificate.')
           
            return redirect('certificate_view', course_id=course.id)
        else:
            messages.error(request, 'You did not pass the test. Please try again.')

        return redirect('course_detail', course_id=course_id)

# View to upload a video for a course
def upload_video(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.course = course
            video.save()
            messages.success(request, 'Video uploaded successfully.')
            return redirect('course_detail', course_id=course.id)
    else:
        form = VideoUploadForm()

    return render(request, 'upload_video.html', {'form': form, 'course': course})

def certificate_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    # Get the Student instance associated with the logged-in user
    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('course_detail', course_id=course.id)

    # Get the certificate for the student and course
    certificate = Certificate.objects.filter(student=student, course=course).first()

    if not certificate:
        messages.error(request, 'No certificate available.')
        return redirect('course_detail', course_id=course.id)

    return render(request, 'certificate.html', {
        'course': course,
        'certificate': certificate,  # Pass a single certificate object
    })
from .models import Video, Comment
def add_comment(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Video, id=video_id)
        comment_text = request.POST.get('comment')

        if comment_text:
            Comment.objects.create(
                video=video,
                user=request.user,
                text=comment_text
            )
            messages.success(request, 'Your comment has been posted.')
        else:
            messages.error(request, 'Comment cannot be empty.')

    return redirect('course_detail', course_id=video.course.id)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Certificate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4

def download_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{certificate.id}.pdf"'
    
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Set background color.
    p.setFillColor(colors.whitesmoke)
    p.rect(0, 0, width, height, fill=True, stroke=False)

    # Logo section:
    logo_path = r"C:\Users\LENOVO\CourseRegistrationPorta\courses\jntu.png" # Update with your actual logo path.
    try:
        logo = ImageReader(logo_path)
        
        # Option 1: Directly set the width and height.
        # Modify these numbers to make your logo larger or smaller.
        logo_width = 100  # set desired width (points)
        logo_height = 75  # set desired height (points)
        p.drawImage(logo, 50, height - 150, width=logo_width, height=logo_height, mask='auto')
        
        # Option 2: Maintain aspect ratio using the original image dimensions.
        # Uncomment this section if you want to scale proportionally.
        # original_logo_width, original_logo_height = logo.getSize()
        # scale_factor = 0.5  # change the factor based on your need (0.5 is 50%)
        # scaled_width = original_logo_width * scale_factor
        # scaled_height = original_logo_height * scale_factor
        # p.drawImage(logo, 50, height - 150, width=scaled_width, height=scaled_height, mask='auto')

    except Exception as e:
        # If the logo isn't available, handle the exception gracefully.
        pass
    p.setFont("Helvetica-Bold", 15)
    p.setFillColor(colors.black)
    p.drawCentredString(width/2.0, height-110, "   Jawaharlal Nehru Technological University -")
    p.drawCentredString(width/2.0, height-130, "Gurajada, Vizianagaram")


    # Certificate content.
    p.setFont("Helvetica-Bold", 36)
    p.setFillColor(colors.darkblue)
    p.drawCentredString(width/2.0, height-200, "Certificate of Achievement")

    p.setFont("Helvetica", 20)
    p.setFillColor(colors.black)
    p.drawCentredString(width/2.0, height-260, f"This certifies that {certificate.student.user.username}")

    p.setFont("Helvetica-Oblique", 16)
    p.drawCentredString(width/2.0, height-300, f"has successfully completed the course {certificate.course.name}")

    p.setFont("Helvetica", 16)
    p.drawCentredString(width/2.0, height-340, f"on {certificate.date_issued.strftime('%d %B %Y')}")

    p.setLineWidth(4)
    p.setStrokeColor(colors.darkblue)
    p.rect(50, 50, width-100, height-100)

    p.showPage()
    p.save()
    return response
import cv2
import face_recognition
import numpy as np
from django.http import StreamingHttpResponse
from django.views.decorators import gzip

# Function to calculate Eye Aspect Ratio (EAR)
def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def detect_face(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_landmarks_list = face_recognition.face_landmarks(rgb_frame)
    
    if len(face_landmarks_list) == 0:
        return frame, False  # No face detected

    for face_landmarks in face_landmarks_list:
        left_eye = np.array(face_landmarks['left_eye'])
        right_eye = np.array(face_landmarks['right_eye'])

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        # Draw landmarks (optional)
        for (x, y) in left_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        for (x, y) in right_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        # Check if eyes are open
        if left_ear < 0.2 or right_ear < 0.2:
            return frame, True  # Eyes closed

    return frame, False  # Normal state

def generate_frames():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    
    while True:
        success, frame = camera.read()
        if not success:
            break
            
        frame, alert = detect_face(frame)
        
        # Add status text to frame
        status_text = "ALERT: Not Paying Attention!" if alert else "Normal"
        color = (0, 0, 255) if alert else (0, 255, 0)
        cv2.putText(frame, status_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    camera.release()

@gzip.gzip_page
def video_feed(request):
    return StreamingHttpResponse(
        generate_frames(),
        content_type="multipart/x-mixed-replace;boundary=frame"
    )
def submit_test(request, course_id):
    # Check for inappropriate movements from session
    inappropriate_movement = request.session.get('inappropriate_movement', False)
    
    if inappropriate_movement:
        # Clear the flag after detection
        request.session['inappropriate_movement'] = False
        request.session.modified = True
        
        messages.error(request, 'Test submission rejected due to suspicious activity.')
        return redirect('course_detail', course_id=course_id)

    # Rest of your existing test submission logic
    course = get_object_or_404(Course, id=course_id)
    test = course.test

    if request.method == 'POST':
        questions = test.questions.all()
        score = 0

        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option == question.correct_option:
                score += 1

        if score >= test.pass_mark:
            try:
                student = Student.objects.get(user=request.user)
            except Student.DoesNotExist:
                messages.error(request, 'Student profile not found.')
                return redirect('course_detail', course_id=course.id)

            certificate = Certificate.objects.filter(student=student, course=course).first()

            if not certificate:
                certificate = Certificate.objects.create(student=student, course=course, score=score)
                messages.success(request, 'Congratulations! You passed the test and earned a certificate.')
            else:
                messages.info(request, 'You have already earned a certificate for this course.')

            return redirect('certificate_view', course_id=course.id)
        else:
            messages.error(request, 'You did not pass the test. Please try again.')
            return redirect('course_detail', course_id=course_id)

    return redirect('course_detail', course_id=course_id)