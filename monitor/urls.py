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
    path('question_details/<int:obj_id>', views.question_details, name='question_details'),
    path('all_question/', views.all_question, name='all_question'),
    path('develop_questions/', views.develop_questions, name='develop_questions'),
    path('student_profile/', views.student_userbio, name='student_profile'),
    path('teacher_profile/', views.teacher_userbio, name='teacher_profile'),
    path('courses/', views.create_courses, name='courses'),
    path('all_courses/', views.all_courses, name='all_courses'),
    path('responses/<int:obj_id>', views.submitted_responses, name='responses'),
    path('take_tests/<int:obj_id>', views.take_tests, name='take_tests'),
    path('get_student_level_courses/<str:level>', views.get_student_level_courses, name='get_student_level_courses'),
    path('student_tests/', views.student_tests, name='student_tests'),
    path('completed_test/', views.completed_test, name='completed_test'),
    path('results/<int:obj_id>', views.results, name='results'),
    path('teacher_results/<int:ques_id>/<int:student_id>', views.teacher_view_results, name='teacher_results'),
	]