import email
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from . models import Department
import pdb;
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from validate_email import validate_email
import threading
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send(fail_silently=False)


def DashboardView(request):
    return render (request, 'Admin_Dashboard/Dashboard.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def AddEmployeeView(request):
    if request.method == "POST":
        name = request.POST['username']
        email = request.POST['email']
        number = request.POST['number'] 
        department = request.POST['department'] 
        date = request.POST['date'] 
        password = request.POST['password'] 
        user = User.objects.create_user(username=name, email=email, first_name=number, last_name=department, date_joined=date )
        user.set_password(password)
        user.is_active = True
        user.save()
        current_site = get_current_site(request)
        email_subject = 'Welcome to our company!'
        email = EmailMessage(
            email_subject,
            'Hi, '+user.username + ', we\'re glad that you\'ve joined our company. Below are your credentials to log in to our website. \n'+
            '\nUsername: '+name+
            '\nEmail: '+email+
            '\nPassword: '+password+
            '\nYour date of joining as registered with us is '+date+
            '\nHere\'s the link to our company\'s website: '+'https://'+current_site.domain,
            'noreply@semycolon.com',
            [email],
        )
        EmailThread(email).start()
        messages.success(request, 'Employee added successfully!')
        return redirect('nDashboard')
    if request.method=="GET":
        obj = Department.objects.all()
        return render (request, 'Admin_Dashboard/AddEmployee.html', {'obj':obj})



def SettingsView(request):
    obj = Department.objects.all()
    return render (request,'Admin_Dashboard/Settings.html', {'obj':obj})


def AddDepartmentView(request):
    if request.method =="POST":
        department = request.POST['department']
        Department.objects.create(dept=department)
        messages.success(request, 'New department added successfully!')
        return redirect('nsettings')
    else:
        messages.error(request, 'You tried accessing a prohibited page')
        return redirect('nDashboard')

def DeleteDepartmentView(request):
    if request.method=="POST":
        dept = request.POST['dept']
        print(dept)
        obj = Department.objects.get(dept=dept)
        obj.delete()
        messages.success(request, 'Department deleted successfully!!')
        return redirect('nsettings')
    else:
        messages.error(request, 'You tried accessing a prohibited page')
        return redirect('nDashboard')


def ValidateEmployeeUsernameView(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters!'})
        exists = User.objects.filter(username=username).exists()
        if exists:
            return JsonResponse({'username_error': 'Sorry! This username in use, choose another one!'})
        return JsonResponse({'username_valid': True})
    else:
        messages.error(request, 'You are accessing a prohibited page!!')
        return redirect('nDashboard')


def ValidateEmployeeEmailView(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry email in use, choose another one'})
        return JsonResponse({'email_valid': True})
    else:
        messages.error(request, 'You tried accessing a prohibited page!!')
        return redirect('nDashboard')




