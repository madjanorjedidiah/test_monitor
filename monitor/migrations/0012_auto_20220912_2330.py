# Generated by Django 3.0.7 on 2022-09-12 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0011_auto_20220912_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='course_fk',
            field=models.ManyToManyField(related_name='student_course', to='monitor.Courses'),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='course_fk',
            field=models.ManyToManyField(related_name='teacher_course', to='monitor.Courses'),
        ),
    ]