# courses/forms.py
from django import forms
from .models import Video
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# courses/forms.py


class SemesterForm(forms.Form):
    semester = forms.ChoiceField(choices=[('1', '1st Semester'), ('2', '2nd Semester')], label="Select Semester")
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
def clean_password2(self):
        # Bypass password validation
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2
# Login Form
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file', 'duration']

class SearchForm(forms.Form):
    query = forms.CharField(
        label='Search courses',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Search courses...'})
    )