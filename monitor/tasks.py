from celery import shared_task
import os
from celery.result import AsyncResult
from .helpers import send_mail, current_time, wait_time, take_screen_shot, mk_directory, get_user, distribute_marks_for_each_question, is_equal
import time
from django.db.models import Sum
from .models import *



@shared_task
def execute_take_screenshot(student_user, duration=60, sec=None):
    directory = mk_directory(student_user)
    start_time = time.time()
    elapsed = 0
    wait = 0
    while elapsed < duration:
        elapsed = time.time() - start_time
        now = current_time()
        take_screen_shot(os.path.join(directory, now))
        send_email = send_mail(
            'jmadjanor6@gmail.com', 
            student_user, 
            'Current Screenshots', 
            now, 
            f'{os.path.join(directory, now)}.png'
        )
        wait_time(sec)
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
    return True



@shared_task
def total_score(ques_id, student_id):
    tot_score = Answers.objects.filter(student_fk_id=student_id).aggregate(Sum('marks'))
    Results.objects.update_or_create(
        question_fk_id=ques_id, 
        score=tot_score['marks__sum'], 
        student_fk_id=student_id
    )
    return True



def capture_images():
    cam = VideoCapture(0)
    result, image = cam.read()  

    # show the image
    if result:
        imshow("GeeksForGeeks", image)

        # save the image
        imwrite("GeeksForGeeks.png", image)

    else:
        print("No image detected. Please! try again")   

