from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser
from courses.models import Registration
from .forms import StudentProfileForm
from .models import Student

def dashboard(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # If authenticated, fetch the student's registrations
        try:
            student = request.user.student  # Access the logged-in student
            registrations = Registration.objects.filter(student=student)
            return render(request, 'dashboard.html', {'registrations': registrations})
        except AttributeError:
            # Handle case where the Student profile does not exist
            return render(request, 'dashboard.html', {'error': 'Student profile not found.'})
    else:
        # If not authenticated, display a message or redirect
        return render(request, 'dashboard.html', {'error': 'Please log in to view your dashboard.'})
def update_profile(request):
    student = request.user.student  # Get the logged-in student's profile

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the profile page
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'update_profile.html', {'form': form})
def home(request):
    try:
        # Check if the user already has a Student profile
        student = request.user.student
        # If the profile exists, redirect to the dashboard or another page
        return redirect('dashboard')  # Replace 'dashboard' with the appropriate URL name
    except Student.DoesNotExist:
        # If the profile does not exist, show the profile creation form
        if request.method == 'POST':
            form = StudentProfileForm(request.POST)
            if form.is_valid():
                # Create a Student profile for the user
                student = form.save(commit=False)
                student.user = request.user
                student.save()
                return redirect('dashboard')  # Redirect to the dashboard after profile creation
        else:
            form = StudentProfileForm()

        return render(request, 'home.html', {'form': form})