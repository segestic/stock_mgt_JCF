from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied

def unauthenticated_user(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_teacher:
                return HttpResponseRedirect(reverse('select_item'))
            elif request.user.is_manager:
                return HttpResponseRedirect(reverse('list_item'))
        else:
            return view_func(request, *args, **kwargs)
    return wrap


def teacher_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_teacher:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('/'))
    return wrap

def manager_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_manager:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('select_item'))
    return wrap