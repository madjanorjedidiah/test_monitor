from celery import shared_task
import os
from celery.result import AsyncResult
from .helpers import (current_time, 
    wait_time, 
    take_screen_shot, 
    mk_directory, 
    get_user, 
    distribute_marks_for_each_question, 
    is_equal, 
    web_cam_capture,
    get_student_results,
    send_mail
    )
import time
from django.db.models import Sum
from .models import *
import cv2




@shared_task
def execute_monitor(teacher, student_user, duration=60, sec=None):
    directory = mk_directory(student_user)
    start_time = time.time()
    elapsed = 0
    wait = 0
    while elapsed < duration:
        elapsed = time.time() - start_time
        now = current_time()
        take_screen_shot(os.path.join(directory, now))
        wait_time(sec)
        web_cam_capture(os.path.join(directory, now))
        if sec:
            wait += sec
            elapsed = elapsed - wait
    return 'done'


@shared_task
def assign_marks(user_id, ques_id):
    all_answers = Answers.objects.filter(
        sub_question_fk__question_fk=ques_id,
        student_fk__user_fk_id=user_id)
    even_marks = distribute_marks_for_each_question(ques_id)
    for aa in range(0, len(all_answers)):
        if is_equal(all_answers[aa].sub_question_fk.correct_answer, all_answers[aa].answer):
            all_answers[aa].marks = even_marks
            all_answers[aa].save()
        else:
            all_answers[aa].marks = 0
            all_answers[aa].save()
    return 'done'



@shared_task
def total_score(ques_id, student_id):
    tot_score = Answers.objects.filter(student_fk_id=student_id).aggregate(Sum('marks'))
    Results.objects.update_or_create(
        question_fk_id=ques_id, 
        score=tot_score['marks__sum'], 
        student_fk_id=student_id
    )
    return 'done'


@shared_task
def send_teacher_results(teacher_mail, teacher_name, student_name, student_id, ques_id):
    student_results = get_student_results(student_id, ques_id)[1][0].score
    send_mail(
        teacher_mail,
        """ Students Results Submitted """,
        """Dear """+ teacher_name +  """
    You are receiving this email because """+ student_name + """ has just submitted the test answers. 
    Find below the graded results for the answers submitted. 
    Thank you.""" 
    """ Score: """ +   str(student_results) +"""
    Click the link to view details of the results, url: teacher_results/""" + f'{ques_id}' + '/' + f'{student_id}'
    """This is an auto-generated mail and therefore does not require a response. """
    )
    return 'done'