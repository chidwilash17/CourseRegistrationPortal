# run.py
import os
import sys
from django.core.management import execute_from_command_line

if __name__ == "_main_":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CourseRegistrationPorta.settings")
    execute_from_command_line([sys.argv[0], "runserver", "0.0.0.0:8000"])