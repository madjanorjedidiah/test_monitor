# Generated by Django 3.0.7 on 2022-09-19 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0015_auto_20220917_0045'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answers',
            old_name='question_fk',
            new_name='sub_question_fk',
        ),
        migrations.AddField(
            model_name='answers',
            name='marks',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]