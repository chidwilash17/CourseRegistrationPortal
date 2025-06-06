# Generated by Django 4.2.20 on 2025-03-14 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0006_submission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='date_issued',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
