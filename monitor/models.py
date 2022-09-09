from django.db import models
from django.contrib.auth.models import AbstractUser


class UserIdentity(AbstractUser):
	accnt_type = (('questioner','questioner'),('candidate','candidate'))
	contact = models.CharField(max_length=13, null=True, blank=True)
	acount_type = models.CharField(choices=accnt_type, max_length=15, null=True, blank=True)


class Question(models.Model):
	question_title = models.CharField(max_length=200, null=True, blank=True)
	user_fk = models.ForeignKey(UserIdentity, on_delete=models.CASCADE)

	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return self.question


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
	user_fk = models.ForeignKey(UserIdentity, on_delete=models.CASCADE)


	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return self.answer
