from .models import *


def get_user(request,):
    user = None
    user_set = UserIdentity.objects.filter(username=request.user)
    if len(user_set) > 0:
        user = user_set[0]
    return user


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