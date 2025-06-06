# Generated by Django 4.2.20 on 2025-03-15 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_alter_course_semester'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration',
            old_name='date_registered',
            new_name='registered_at',
        ),
        migrations.AddField(
            model_name='registration',
            name='semester',
            field=models.CharField(choices=[('1', '1st Semester'), ('2', '2nd Semester')], default='1', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='registration',
            name='status',
            field=models.CharField(choices=[('registered', 'Registered'), ('waitlisted', 'Waitlisted')], max_length=20),
        ),
    ]
