# Generated by Django 3.0.7 on 2022-09-12 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0007_auto_20220912_0054'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(blank=True, max_length=4, null=True)),
                ('course_code', models.CharField(blank=True, max_length=200, null=True)),
                ('caourse_name', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='students',
            name='course_fk',
            field=models.ManyToManyField(to='monitor.Courses'),
        ),
        migrations.AddField(
            model_name='teachers',
            name='course_fk',
            field=models.ManyToManyField(to='monitor.Courses'),
        ),
    ]