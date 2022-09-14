from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .forms import *
from django.contrib.auth.decorators import login_required
from . helpers import get_user, format_multiple_answers


def signup(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		user_role = request.POST.get('user_role')
		password = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')
		if password == confirm_password:
			user, created = UserIdentity.objects.get_or_create(username=username.lower(), email=email.lower(), user_role=user_role)
			if created:
				user.set_password(password)
				user.save()
				if user_role == 'teacher':
					teacher_data, created = Teachers.objects.get_or_create(user_fk_id = user.id)
				else:
					student_data, created = Students.objects.get_or_create(user_fk_id = user.id)
				messages.add_message(
					request, 
					messages.INFO,
					"You have successfully signed up",
					extra_tags = 'success')
				return HttpResponseRedirect(reverse('login'))
			messages.add_message(
				request,
				messages.INFO,
				'User already exists',
				extra_tags = 'danger')
		messages.add_message(
				request,
				messages.INFO,
				'Passwords do not match',
				extra_tags = 'danger')
	return render(request, 'monitor/signup.html')



# ##################   Login view   ##########################################
def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =  request.POST.get('password')

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			if user.is_superuser:
				return HttpResponseRedirect(reverse('admin_level'))

			return HttpResponseRedirect(reverse('profile'))	
		messages.add_message(
				request,
				messages.INFO,
				'Incorrect credentials',
				extra_tags = 'danger')	
	return render(request, 'monitor/login.html')



# ##################   Logout view   ##########################################
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))



def index(request):
	return render(request, 'monitor/index.html')



@login_required(login_url="/login/")
def dashboard(request):
	role_dict = {}
	data_table = UserIdentity.objects.all()
	return render(request, 'monitor/dashboard.html', {"data_table": data_table})



@login_required(login_url="/login/")
def admin_level(request):
	return render(request, 'monitor/admin.html', {'data':UserIdentity.objects.all()})



@login_required(login_url="/login/")
def profile(request):
	user = get_user(request)
	data_table = None
	if user.user_role == 'teacher':
		data_table = Teachers.objects.filter(user_fk=user)[0].course_fk.all()[:6]
	else:
		data_table = Students.objects.filter(user_fk=user)[0].course_fk.all()[:6]
	return render(request, 'monitor/profile.html', {'data':user, 'data_table':data_table})



@login_required(login_url="/login/")
def userbio(request):
	user = get_user(request)
	if user.user_role == 'teacher':
		return HttpResponseRedirect(reverse('teacher_profile'))
	else:
		return HttpResponseRedirect(reverse('student_profile'))



@login_required(login_url="/login/")
def student_userbio(request):
	user = get_user(request)
	all_course = Courses.objects.filter(level=level)
	if request.method == 'POST':
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		contact = request.POST.get('contact')
		level = request.POST.get('level')
		courses = request.POST.getlist('courses')
		user.first_name = first_name
		user.last_name = last_name
		user.contact = contact
		user.level = level
		user.save()
		student_data = Students.objects.get(user_fk_id = user.id)
		student_data.course_fk.add(*courses)
		messages.add_message(
			request, 
			messages.INFO,
			"You have successfully updated your record",
			extra_tags = 'success'
		)
		return HttpResponseRedirect(reverse('profile'))
	return render(request, 'monitor/student_userbio.html', {'all_course':all_course})



#@login_required(login_url="/login/")
def teacher_userbio(request):
	all_course = Courses.objects.all()
	if request.method == 'POST':
		user = get_user(request)
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		contact = request.POST.get('contact')
		courses = request.POST.getlist('courses')
		user.first_name = first_name
		user.last_name = last_name
		user.contact = contact
		user.save()
		teacher_data = Teachers.objects.get(user_fk_id = user.id)
		teacher_data.course_fk.add(*courses)
		messages.add_message(
			request, 
			messages.INFO,
			"You have successfully updated your record",
			extra_tags = 'success'
		)
		return HttpResponseRedirect(reverse('profile'))
	return render(request, 'monitor/teacher_userbio.html', {'all_course':all_course})



# ///////////////////////////   delete a user  /////////////////////////
def deleteuser(request, obj_id):
	idd = request.GET.get('data')
	user = UserIdentity.objects.get(id=idd)
	user.delete()
	return HttpResponse('done')



# ///////  account closed   ///////////
def close_account(request):
	user = get_user(request)
	user.delete()
	return HttpResponse('User account has successfully been closed')




def question_index(request):
	return render(request, 'monitor/questions_index.html', {'data': Question.objects.filter(user_fk=get_user(request))[:3]})



def question_details(request, obj_id):
	return render(request, 'monitor/question_details.html', {'data': Question.objects.filter(id=obj_id)})



def all_question(request):
	user = get_user(request)
	data = None
	if user.user_role == 'teacher':
		data = Question.objects.filter(teacher_fk__user_fk=user)
	return render(request, 'monitor/all_questions.html', {'data':data})



def submitted_responses(request):
	obj_id = request.GET.get('data')
	user = get_user(request)
	data = None
	if user.user_role == 'teacher':
		data = Answers.objects.filter(question_fk_id=obj_id)
		print(data)
	return render(request, 'monitor/submitted_responses.html', {'data':data})


# ////////////  create questions
def develop_questions(request):
	obj_id = request.GET.get('data')
	course = None
	if obj_id:
		course = Courses.objects.filter(id=obj_id)
	if request.method == 'POST':
		question_title = request.POST.get('question_title')
		question = request.POST.getlist('question')
		multiple_answers = request.POST.getlist('multiple_answers')
		correct_answer = request.POST.getlist('correct_answer')
		diviser = request.POST.get('diviser')
		level = request.POST.get('level')
		course_code = request.POST.get('course_code')
		multi_ans = format_multiple_answers(diviser, multiple_answers)
		ziped = list(zip(question, multi_ans, correct_answer))
		if course == None:
			course = Courses.objects.filter(level=level, course_code=course_code)
		ques_data, created = Question.objects.get_or_create(
			question_title=question_title, 
			teacher_fk_id=Teachers.objects.get(user_fk=get_user(request)).id, 
			course_fk_id=course[0].id if course else course)
		if created:
			for a in range(0,len(ziped)):
				SubQuestions.objects.get_or_create(
					question = ziped[a][0],
					question_fk_id = ques_data.id,
					defaults = {
						'multiple_answers': ', '.join(ziped[a][1]),
						'correct_answer': ziped[a][2]
					}
				)
			messages.add_message(
				request, 
				messages.INFO,
				"You have successfully created your record",
				extra_tags = 'success'
			)
			return HttpResponse('done')
		else:
			messages.add_message(
				request, 
				messages.INFO,
				"Question already exists",
				extra_tags = 'success'
			)
	return render(request, 'monitor/questions_form.html', {'course_data':course[0] if course else course})



def create_courses(request):
	if request.method == 'POST':
		course_name = request.POST.get('course_name')
		level = request.POST.get('level')
		course_code = request.POST.get('course_code')
		semester = request.POST.get('semester')
		data, created = Courses.objects.get_or_create(course_name=course_name, course_code=course_code, defaults={'level': level, 'semester': semester})
		if created:
			messages.add_message(
				request, 
				messages.INFO,
				"You have successfully created your record",
				extra_tags = 'success'
			)
	return render(request, 'monitor/courses_form.html')



# ///////////  take in candidate answers
def get_responses(request):
	obj_id = request.GET.get('data')
	question_data = Question.objects.filter(id=obj_id)
	if request.method == 'POST':
		answer = request.POST.get('answer')
		subquestions_id = request.POST.get('subquestions_id')
		data, created = Answers.objects.get_or_create(answer=answer, question_fk_id=subquestions_id, defaults={'student_fk_id': get_user(request).id})
		if created:
			messages.add_message(
				request, 
				messages.INFO,
				"You have successfully submitted a response",
				extra_tags = 'success'
			)
	return render(request, 'monitor/answers_form.html', {'question_data':question_data})



## /////////  render marks for candidate


# //////////  



def all_courses(request):
	return render(request, 'monitor/all_courses.html', {'courses':Courses.objects.all()})