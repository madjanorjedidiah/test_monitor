from . import views 
from django.urls import path


urlpatterns = [
	path('', views.index, name='home'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('login/', views.login_view, name='login'),
	path('signup/', views.signup, name='signup'),
	path('logout/', views.logout_view, name='logout'),
	path('admin_level/', views.admin_level, name='admin_level'),
	path('userbio/', views.userbio, name='userbio'),
	path('profile/', views.profile, name='profile'),
    path('deleteuser/<int:obj_id>', views.deleteuser, name='deleteuser'),
    path('question_index/', views.question_index, name='question_index'),
    path('question_details/', views.question_details, name='question_details'),
    path('all_question/', views.all_question, name='all_question'),
    path('develop_questions/', views.develop_questions, name='develop_questions'),
	]