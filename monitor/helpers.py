from .models import *


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