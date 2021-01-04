from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import TeacherSignUpForm, ManagerSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .decorators1 import unauthenticated_user
# from django.http import HttpResponseRedirect
# from django.urls import reverse


# Create your views here.

@unauthenticated_user
def register(request):
    # if request.user.is_authenticated:
    #     if request.user.is_teacher:
    #         return HttpResponseRedirect(reverse('select_item'))
    #     elif request.user.is_manager:
    #         return HttpResponseRedirect(reverse('list_item'))
    return render(request, '../templates/register.html')

# @unauthenticated_user
class teacher_register(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = '../templates/teacher_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('select_item')

# @unauthenticated_user
class manager_register(CreateView):
    model = User
    form_class = ManagerSignUpForm
    template_name = '../templates/manager_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('list_item')

@unauthenticated_user
def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                if user.is_teacher:
                    login(request,user)
                    return redirect('select_item')
                elif user.is_manager:
                    login(request, user)
                    return redirect('list_item')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')