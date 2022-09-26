from .models import *
from dateutil.parser import parse
from django.http import HttpResponse
from django.db.models import Sum
import time
from datetime import datetime
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import cv2
from psutil import Process
import base64
import json  
from test_monitor.celery import app as celery_app
from PIL import ImageGrab
from test_monitor.settings import MEDIA_ROOT




# Load dotenv
load_dotenv()


def get_user(request,):
    user = None
    user_set = UserIdentity.objects.filter(username=request.user)
    if len(user_set) > 0:
        user = user_set[0]
    return user


# create a sublist from a list with the lenth of the sublist equal to the n target 
def list_sub_list(lst, n):
    newl = []
    start_index = 0
    end_index = n
    if len(lst)>n:
        floor_division = len(lst)//n
        modulo = len(lst)%n
        for ad in range(floor_division):
            newl.append(lst[start_index:end_index])
            start_index = end_index
            end_index += n
        if modulo:
            newl.append(lst[end_index-n:])
    else:
        newl.append(lst)
    return newl


# format multiple answes into right list format
def format_multiple_answers(diviser: str, lists: list):
    c = 0
    new_list = []
    for a in diviser:
        if a == '0':
            new_list.append([])
        elif diviser.index(a) == 0:
            new_list.append(lists[c:int(a)])
            c += int(a)
        else:
            new_list.append(lists[c:int(a)+int(c)])
            c += int(a)
    return new_list



def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def distribute_marks_for_each_question(ques_id):
    question = Question.objects.filter(id=ques_id)
    if question:
        su_ques_lenght = len(question[0].subquestions_set.all())
        return round(100 / su_ques_lenght, 0)
    return None



def is_equal(a, b):
    return True if a.lower() == b.lower() else False




def take_screen_shot(func):
    myscreen = ImageGrab.grab()  #pyautogui.screenshot()
    return myscreen.save(f'{func}.png')



def wait_time(sec=None):
    if sec == None:
        sec = 8
    return time.sleep(sec)



def current_time():
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    return current_time



def send_mail_image(send_to, subject, text, text_name, file=None):
    msg = MIMEMultipart()
    msg['From'] = os.environ.get('USER')
    msg['To'] = send_to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    ff = open(file, "rb")
    part = MIMEApplication(
        ff.read(),
        Name=basename(file)
    )
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % text_name+'.png'
    msg.attach(part)
    server = smtplib.SMTP(os.environ.get('HOST'), os.environ.get('PORT'))
    server.starttls()
    server.login(os.environ.get('USER_MAIL'), os.environ.get('PASSWORD'))
    server.sendmail(os.environ.get('USER_MAIL'), send_to, msg.as_string())
    server.close()
    return 'email_sent'



def mk_directory(name):
    # Create a new folder called 'Results' 
    result_folder = os.path.join(MEDIA_ROOT, name)

    # Check if the folder exists already
    if not os.path.exists(result_folder):
        
        print("Creating a folder for the results..")
        # If it does not exist, create one
        os.makedirs(result_folder)
        print(result_folder, "folder created")  
    else:
        print("Results folder exists already.")
    return result_folder



def format_seconds(hr):
    return 60 * 60 * hr


def format_string(a):
    return a.replace(" ","")



def web_cam_capture(name):
    cam = cv2.VideoCapture(0)
    result, image = cam.read()  

    # show the image
    if result:
        # save the image
        cv2.imwrite(f"{name}_snapshot.png", image)
    else:
        print("No image detected. Please! try again")  
    return True 



def get_teacher_mail(ques_id):
    question = Question.objects.filter(id=ques_id)
    if question:
        return question[0].teacher_fk.user_fk.email
    return False



def get_student_results(student_id, ques_id):
    question_data = Question.objects.filter(id=ques_id)
    ans = Answers.objects.filter(
        sub_question_fk__question_fk=question_data[0].id,
        student_fk=student_id) 
    total_marks = Results.objects.filter(question_fk_id=question_data[0].id)
    return (ans, total_marks, student_id)



def send_mail(send_to, subject, text):
    msg = MIMEMultipart()
    msg['From'] = os.environ.get('USER_MAIL')
    msg['To'] = send_to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    # After the file is closed
    server = smtplib.SMTP(os.environ.get('HOST'), os.environ.get('PORT'))
    server.starttls()
    server.login(os.environ.get('USER_MAIL'), os.environ.get('PASSWORD'))
    server.sendmail(os.environ.get('USER_MAIL'), send_to, msg.as_string())
    server.close()
    return 'email_sent'