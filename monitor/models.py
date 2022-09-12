from django.db import models
from django.contrib.auth.models import AbstractUser


class UserIdentity(AbstractUser):
	user_type = (('teacher', 'teacher'), ('student', 'student'))
	contact = models.CharField(max_length=13, null=True, blank=True)
	user_role = models.CharField(choices=user_type, max_length=20)


class Teachers(models.Model):
	user_fk = models.OneToOneField(UserIdentity, on_delete=models.CASCADE, related_name='user_teacher')
	created_at = models.DateTimeField(auto_now_add=True, null=True)


	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return self.name


class Students(models.Model):
	level = models.CharField(max_length=4, null=True, blank=True)
	user_fk = models.OneToOneField(UserIdentity, on_delete=models.CASCADE, related_name='user_student')
	created_at = models.DateTimeField(auto_now_add=True, null=True)


	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return self.name


class Question(models.Model):
	question_title = models.CharField(max_length=200, null=True, blank=True)
	level = models.CharField(max_length=4, null=True, blank=True)
	semester = models.CharField(max_length=4, null=True, blank=True)
	year = models.CharField(max_length=4, null=True, blank=True)
	teacher_fk = models.ForeignKey(Teachers, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, null=True)


	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return self.question_title


class SubQuestions(models.Model):
	question = models.CharField(max_length=1000, null=True, blank=True)
	multiple_answers = models.CharField(max_length=1000, null=True, blank=True)
	correct_answer = models.CharField(max_length=1000, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	question_fk = models.ForeignKey(Question, on_delete=models.CASCADE)


	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return self.question


class Answers(models.Model):
	answer = models.CharField(max_length=1000, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	question_fk = models.ForeignKey(SubQuestions, on_delete=models.CASCADE)
	student_fk = models.ForeignKey(Students, on_delete=models.CASCADE)


	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return self.answer
