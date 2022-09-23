from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .forms import *
from django.contrib.auth.decorators import login_required
from . helpers import *
from .tasks import *
from test_monitor.celery import app as celery_app
from django.db.models import Max, Avg, Count, Min, Sum



def signup(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		user_role = request.POST.get('user_role')
		password = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')
		if password == confirm_password:
			user, created = UserIdentity.objects.get_or_create(
				username=username.lower(), 
				email=email.lower(), 
				user_role=user_role
			)
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
	role_dict, gender_dict, scores, course_student, course_score = {}, {}, {}, {}, {}
	data_table = UserIdentity.objects.all()
	role_dict['teacher'] = len(data_table.filter(user_role='teacher'))
	role_dict['student'] = len(data_table.filter(user_role='student'))
	gender_dict['male'] = len(data_table.filter(gender='male'))
	gender_dict['female'] = len(data_table.filter(gender='female'))
	questions_served = Question.objects.count()
	answers_served = Answers.objects.count()
	res = Results.objects.all()
	scores['max'] = res.aggregate(Max('score'))['score__max']
	scores['min'] = res.aggregate(Min('score'))['score__min']
	course = res.values('question_fk__course_fk__course_code').annotate(num_students=Count('student_fk_id'))
	max_stu = course.aggregate(Max('num_students'))['num_students__max']
	min_stu = course.aggregate(Min('num_students'))['num_students__min']
	course_student['course_with_max_students'] = course.filter(num_students=max_stu)[0]
	course_student['course_with_min_students'] = course.filter(num_students=min_stu)[0]
	sum_course = res.values('question_fk__course_fk__course_code').annotate(sum_score=Sum('score'))
	high_course_score = sum_course.aggregate(Max('sum_score'))['sum_score__max']
	low_course_score = sum_course.aggregate(Min('sum_score'))['sum_score__min']
	course_score['course_with_high_scores'] = sum_course.filter(sum_score=high_course_score)[0]
	course_score['course_with_low_scores'] = sum_course.filter(sum_score=low_course_score)[0]
	context = {
	"data_table": data_table, 
	'role':role_dict, 
	'gender':gender_dict,
	'questions_served': questions_served,
	'answers_served': answers_served,
	'scores': scores,
	"course_student":course_student,
	'course_score': course_score
	}
	return render(request, 'monitor/dashboard.html', context)



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
	all_course = None # Courses.objects.filter(level=level)
	if request.method == 'POST':
		first_name = request.POST.get('first_name', user.first_name)
		last_name = request.POST.get('last_name', user.last_name)
		gender = request.POST.get('gender', user.gender)
		contact = request.POST.get('contact', user.contact)
		courses = request.POST.getlist('courses')
		level = request.POST.get('level')
		user.first_name = first_name
		user.last_name = last_name
		user.gender = gender
		user.contact = contact
		user.save()
		student_data1 = Students.objects.get(user_fk_id = user.id)
		student_data1.level = level
		student_data1.save()
		student_data1.course_fk.add(*courses)
		messages.add_message(
			request, 
			messages.INFO,
			"You have successfully updated your record",
			extra_tags = 'success'
		)
		return HttpResponseRedirect(reverse('profile'))
	student_data = Students.objects.filter(user_fk=user)
	context = {'all_course':all_course, 'student_data':student_data[0] if student_data else student_data}
	return render(request, 'monitor/student_userbio.html', context)



def get_student_level_courses(request, level):
	all_course = None
	if level:
		all_course = Courses.objects.filter(level=level)
		student_course = Students.objects.filter(user_fk=request.user)
	return render(request, 'monitor/student_course.html', {
		'all_course':all_course, 
		'student_course':student_course[0] if student_course else None})



#@login_required(login_url="/login/")
def teacher_userbio(request):
	all_course = Courses.objects.all()
	teachers_data = Teachers.objects.filter(user_fk=request.user)
	if request.method == 'POST':
		user = get_user(request)
		first_name = request.POST.get('first_name', user.first_name)
		last_name = request.POST.get('last_name', user.last_name)
		gender = request.POST.get('gender', user.gender)
		contact = request.POST.get('contact', user.contact)
		courses = request.POST.getlist('courses')
		user.first_name = first_name
		user.last_name = last_name
		user.contact = contact
		user.gender = gender
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
	context = {'all_course':all_course, 'teachers_data':teachers_data[0] if teachers_data else None}
	return render(request, 'monitor/teacher_userbio.html', context)



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
	return render(request, 'monitor/questions_index.html', {'data': Question.objects.filter(teacher_fk__user_fk=get_user(request))[:3]})



def question_details(request, obj_id):
	return render(request, 'monitor/question_details.html', {'data': Question.objects.filter(id=obj_id)})



def all_question(request):
	user = get_user(request)
	data = None
	if user.user_role == 'teacher':
		data = Question.objects.filter(teacher_fk__user_fk=user)
	return render(request, 'monitor/all_questions.html', {'data':data})



def submitted_responses(request, obj_id):
	submitted = Results.objects.filter(question_fk_id=obj_id)
	return render(request, 'monitor/submitted_responses.html', {'data':submitted})



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
		duration = request.POST.get('duration')
		course_code = request.POST.get('course_code')
		date_scheduled = request.POST.get('date_scheduled')
		show_now = request.POST.get('show_now')
		multi_ans = format_multiple_answers(diviser, multiple_answers)
		ziped = list(zip(question, multi_ans, correct_answer))
		if course == None:
			course = Courses.objects.filter(level=level, course_code=course_code)
		ques_data, created = Question.objects.get_or_create(
			question_title=question_title, 
			duration=duration,
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
			if show_now or date_scheduled:
				ScheduleTest.objects.create(
					date_scheduled=date_scheduled if is_date(date_scheduled) else None, 
					show_now=show_now, 
					question_fk_id=ques_data.id)
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
		data, created = Courses.objects.get_or_create(
			course_name=course_name, 
			course_code=course_code, 
			defaults={
			'level': level, 
			'semester': semester
		})
		if created:
			messages.add_message(
				request, 
				messages.INFO,
				"You have successfully created your record",
				extra_tags = 'success'
			)
	return render(request, 'monitor/courses_form.html')



# ///////////  take in candidate answers
def take_tests(request, obj_id):
	if Results.objects.filter(question_fk_id=obj_id):
		return HttpResponseRedirect(reverse('student_tests'))
	question_data = Question.objects.filter(id=obj_id)
	if request.method == 'POST':
		celery_app.control.revoke(execute_monitor.request.id, terminate=True, signal='SIGKILL')
		user_id = request.user.id
		answer = request.POST.getlist('answer')
		subquestions_id = request.POST.getlist('subquestions_id')
		new_l = list(zip(answer, subquestions_id))
		for a in range(0, len(new_l)):
			data, created = Answers.objects.get_or_create(
				answer=format_string(new_l[a][0]), 
				sub_question_fk_id=new_l[a][1], 
				defaults={
				'student_fk_id': Students.objects.filter(
					user_fk_id=user_id)[0].id})
		messages.add_message(
			request, 
			messages.INFO,
			"You have successfully submitted a response",
			extra_tags = 'success'
		)
		assign_marks.delay(user_id, question_data[0].id)
		total_score.delay(
		question_data[0].id, 
		Students.objects.filter(user_fk_id=user_id)[0].id)
		return HttpResponse(['done', question_data[0].id])
	else:
		if question_data[0].duration:
			durattion = format_seconds(question_data[0].duration)
			execute_monitor.delay(f"{get_user(request).first_name}  {get_user(request).last_name }", durattion)
		else:
			execute_monitor.delay(f"{get_user(request).first_name}  {get_user(request).last_name }")
	return render(request, 'monitor/answers_form.html', {'question_data':question_data})



def student_tests(request):
	user = get_user(request)
	if user.user_role == 'student':
		courses = Students.objects.filter(user_fk=user).values_list('course_fk', flat=True)
		tests = [Question.objects.filter(course_fk_id=a) for a in list(courses)]
	return render(request, 'monitor/student_tests.html', {'tests': tests})



def all_courses(request):
	return render(request, 'monitor/all_courses.html', {'courses':Courses.objects.all()})



def completed_test(request):
	return render(request, 'monitor/completed_test.html')


def results(request, obj_id):
	question_data = Question.objects.filter(id=obj_id)
	ans = Answers.objects.filter(
        sub_question_fk__question_fk=question_data[0].id,
        student_fk__user_fk_id=request.user.id) 
	total_marks = Results.objects.filter(question_fk_id=question_data[0].id)
	return render(request, 'monitor/results.html', {'marks':ans, 'total':total_marks})



def teacher_view_results(request, student_id, ques_id):
	question_data = Question.objects.filter(id=ques_id)
	ans = Answers.objects.filter(
        sub_question_fk__question_fk=question_data[0].id,
        student_fk=student_id) 
	total_marks = Results.objects.filter(question_fk_id=question_data[0].id)
	return render(request, 'monitor/results.html', {'marks':ans, 'total':total_marks})