from django.db import models
from django.contrib.auth.models import AbstractUser


class UserIdentity(AbstractUser):
	user_type = (('teacher', 'teacher'), ('student', 'student'))
	contact = models.CharField(max_length=13, null=True, blank=True)
	user_role = models.CharField(choices=user_type, max_length=20)


class Courses(models.Model):
	level = models.CharField(max_length=4, null=True, blank=True)
	semester = models.CharField(max_length=4, null=True, blank=True)
	course_code = models.CharField(max_length=200, blank=True, null=True)
	course_name = models.CharField(max_length=200, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.course_name


class Teachers(models.Model):
	user_fk = models.OneToOneField(UserIdentity, on_delete=models.CASCADE, related_name='user_teacher')
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	course_fk = models.ManyToManyField(Courses, related_name='teacher_course')


	class Meta:
		ordering = ('-id',)


class Students(models.Model):
	level = models.CharField(max_length=4, null=True, blank=True)
	course_fk = models.ManyToManyField(Courses, related_name='student_course')
	user_fk = models.OneToOneField(UserIdentity, on_delete=models.CASCADE, related_name='user_student')
	created_at = models.DateTimeField(auto_now_add=True, null=True)


	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return self.course_fk


class Question(models.Model):
	question_title = models.CharField(max_length=200, null=True, blank=True)
	duration = models.IntegerField(null=True, blank=True)
	teacher_fk = models.ForeignKey(Teachers, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	course_fk = models.ForeignKey(Courses, on_delete=models.CASCADE)


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
		ordering = ('id',)

	def __str__(self):
		return self.question


class Answers(models.Model):
	answer = models.CharField(max_length=1000, null=True, blank=True)
	marks = models.IntegerField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	sub_question_fk = models.ForeignKey(SubQuestions, on_delete=models.CASCADE)
	student_fk = models.ForeignKey(Students, on_delete=models.CASCADE)


	class Meta:
		ordering = ('id',)

	def __str__(self):
		return self.answer



class ScheduleTest(models.Model):
	show = (('open', 'open'), ('close', 'close'))
	date_scheduled = models.DateTimeField(null=True, blank=True)
	show_now = models.CharField(max_length=10, choices=show, default='close')
	question_fk = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='schedule')



class Results(models.Model):
	question_fk = models.ForeignKey(Question, on_delete=models.CASCADE)
	score = models.IntegerField(null=True, blank=True)
	student_fk = models.ForeignKey(Students, on_delete=models.CASCADE)