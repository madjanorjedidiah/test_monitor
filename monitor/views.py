from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .forms import *
from django.contrib.auth.decorators import login_required
from . helpers import get_user


def signup(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		account_type = request.POST.get('account_type')
		password = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')
		if password == confirm_password:
			user, created = UserIdentity.objects.get_or_create(username=username.lower(), email=email.lower())
			if created:
				user.set_password(password)
				user.save()
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

			return HttpResponseRedirect(reverse('dashboard'))	
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
	user = UserIdentity.objects.filter(username=request.user)
	return render(request, 'monitor/profile.html', {'data':user[0] if user else None})


@login_required(login_url="/login/")
def userbio(request):
	if request.method == 'POST':
		user = UserIdentity.objects.filter(username=request.user)
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		contact = request.POST.get('contact')
		data, created = user.update_or_create(
			id = user[0].id,
            defaults = {
            	"first_name": first_name,
            	"last_name": last_name,
            	"contact": contact,
            }
        )
		if created:
			messages.add_message(
				request, 
				messages.INFO,
				"You have successfully created your record",
				extra_tags = 'success'
			)
		else:
			messages.add_message(
				request, 
				messages.INFO,
				"You have successfully updated your record",
				extra_tags = 'success'
			)
		return HttpResponseRedirect(reverse('profile'))
	return render(request, 'monitor/userbio.html')


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
	return render(request, 'monitor/all_questions.html', {'data': Question.objects.filter(user_fk=get_user(request))})


# ////////////  create questions
def develop_questions(request):
	if request.method == 'POST':
		question_title = request.POST.get('question_title')
		question = request.POST.getlist('question')
		multiple_answers = request.POST.getlist('multiple_answers')
		correct_answer = request.POST.getlist('correct_answer')
		print(multiple_answers)
		print(question)
		ques_data, created = Question.objects.get_or_create(question_title=question_title, user_fk_id=get_user(request).id)
		

		if created:
			# for a in 
			SubQuestions.objects.get_or_create(
				question = question,
				question_fk_id = ques_data.id,
				defaults = {
					'multiple_answers': multiple_answers,
					'correct_answer': correct_answer
				}
			)
	return render(request, 'monitor/questions_form.html')



# ///////////  take in candidate answers




## /////////  render marks for candidate


# //////////  