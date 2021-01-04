from django.urls import path
from .import  views

urlpatterns=[
     path('register/',views.register, name='register'),
     path('teacher_register/',views.teacher_register.as_view(), name='teacher_register'),
     path('manager_register/',views.manager_register.as_view(), name='manager_register'),
     path('',views.login_request, name='login'),
     path('logout/',views.logout_view, name='logout'),
]