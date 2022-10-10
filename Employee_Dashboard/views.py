from django.shortcuts import render, redirect
from django.contrib import messages
from . models import Tasks
import pdb;
import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

def dashboardView(request):
    task = Tasks.objects.filter(owner=request.user)
    return render (request, 'Employee_Dashboard/dashboard.html', {'task':task} )


def AddTaskView(request):
    if request.method=="GET":
        maxdate = datetime.datetime.now()
        maxdate = str(maxdate)
        time = maxdate[11:16]
        maxdate = maxdate[:10]+'T'+time    
        return render(request, 'Employee_Dashboard/AddTask.html', {'maxdate':maxdate})
    if request.method=="POST":
        description = request.POST['description']
        type = request.POST['type']
        Datetime = request.POST['datetime']
        time = request.POST['time']
        Date = str(Datetime)
        Date = Date[:10]
        Tasks.objects.create(owner=request.user,StartDate=Date, Description=description, Type=type, StartTime=Datetime, TimeTaken=time)
        messages.success(request, "Task added successfully")
        return redirect('ndashboard')


cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def GetTodayTasksView(request):
    today = datetime.date.today()
    today = str(today)
    Ttasks = Tasks.objects.filter(owner=request.user, StartDate=today)
    Tfinalrep = {}
    def Tget_type(Ttasks):
        return Ttasks.Type
    Ttask_list = list(set(map(Tget_type, Ttasks)))
    def Tget_type_time(Type):
        Ttime=0
        Tfiltered_by_type = Ttasks.filter(Type=Type)
        for item in Tfiltered_by_type:
            Ttime += item.TimeTaken
        return Ttime

    for x in Ttasks:
        for y in Ttask_list:
            Tfinalrep[y] = Tget_type_time(y)
    return JsonResponse({'Ttype_time_data': Tfinalrep}, safe=False)


cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def GetYestTasksView(request):
    yesterday = (datetime.date.today() - datetime.timedelta(1)).strftime('%Y-%m-%d')    
    Ytasks = Tasks.objects.filter(owner=request.user, StartDate=yesterday)
    Yfinalrep = {}
    def Yget_type(Ytasks):
        return Ytasks.Type
    Ytask_list = list(set(map(Yget_type, Ytasks)))
    def Yget_type_time(YType):
        Ytime=0
        Yfiltered_by_type = Ytasks.filter(Type=YType)
        for item in Yfiltered_by_type:
            Ytime += item.TimeTaken
        return Ytime

    for x in Ytasks:
        for y in Ytask_list:
            Yfinalrep[y] = Yget_type_time(y)
    return JsonResponse({'Ytype_time_data': Yfinalrep}, safe=False)





cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def GetWeeklyTasksView(request):
    yesterday = (datetime.date.today() - datetime.timedelta(1)).strftime('%Y-%m-%d')    
    Wtasks = Tasks.objects.filter(owner=request.user, StartDate=yesterday)
    Wfinalrep = {}
    
    
    def Wget_type(Wtasks):
        return Wtasks.Type
    Wtask_list = list(set(map(Wget_type, Wtasks)))
    
    
    def Wget_type_time(WType):
        Wtime=0
        Wfiltered_by_type = Wtasks.filter(Type=WType)
        for item in Wfiltered_by_type:
            Wtime += item.TimeTaken
        return Wtime

    for x in Wtasks:
        for y in Wtask_list:
            Wfinalrep[y] = Wget_type_time(y)
    return JsonResponse({'Wtype_time_data': Wfinalrep}, safe=False)

def ProfileView(request):
    return render (request,'pages-profile.html')