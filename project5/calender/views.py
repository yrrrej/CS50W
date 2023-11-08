from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
import datetime, json
from django.views.decorators.csrf import csrf_exempt

from .models import User,Event


def leapyear(year):
    if (year % 400 == 0) and (year % 100 == 0):
        return True

    elif (year % 4 ==0) and (year % 100 != 0):
        return True

    else:
        return False

def weekchecker(week,datetime):
    month_with_31=[1,3,5,7,8,10,12]
    feb=2
    new=[]
    new
    for i in week:

        #Spilled to previous month and previous month has 31 days
        if i<1 and int(datetime.strftime('%m'))-1 in month_with_31:
            new.append(i+31)

        #Spilled to previous month and previous month do not have 31 days
        elif i<1 and int(datetime.strftime('%m'))-1 not in month_with_31:
            #If previous month was feb
            if int(datetime.strftime('%m'))-1==feb:
                #If the year is a leap year
                if leapyear(int(datetime.strftime('%Y'))):
                    new.append(i+29)

                else:
                    new.append(i+28)

            else:
                new.append(i+30)
        #Spilled to next month and current month is feb
        elif i>28 and int(datetime.strftime('%m'))==feb:

            if leapyear(int(datetime.strftime('%Y'))):

                if i==29:
                    new.append(i)

                else:
                    new.append(i-29)

            else:
                new.append(i-28)

        #Spilled to next month and current month has 31 days 
        elif i>31 and int(datetime.strftime('%m')) in month_with_31:
            new.append(i-31)

        #Spilled to next month and current month has 30 days 
        elif i>30 and int(datetime.strftime('%m')) not in month_with_31:
            new.append(i-30)

        #Did not spill into other months
        else:
            new.append(i)
    
    return new

def weeks(year,month):
    firstofthemonth=datetime.datetime(year,month,1)
    
    if int(firstofthemonth.strftime('%w'))==0:
        week=[1,2,3,4,5,6,7]
    elif int(firstofthemonth.strftime('%w'))==1:
        week=[0,1,2,3,4,5,6]
    elif int(firstofthemonth.strftime('%w'))==2:
        week=[-1,0,1,2,3,4,5]
    elif int(firstofthemonth.strftime('%w'))==3:
        week=[-2,-1,0,1,2,3,4]
    elif int(firstofthemonth.strftime('%w'))==4:
        week=[-3,-2,-1,0,1,2,3]
    elif int(firstofthemonth.strftime('%w'))==5:
        week=[-4,-3,-2,-1,0,1,2]
    elif int(firstofthemonth.strftime('%w'))==6:
        week=[-5,-4,-3,-2,-1,0,1]

    next5weeks=[week]
    for i in range(5):
        week=list(map(lambda x:x+7,week))
        next5weeks.append(week)


    properweeks=[]
    for i in next5weeks:
        properweeks.append(weekchecker(i,firstofthemonth))
    
    week0=[]
    for i in properweeks[0]:
        if i>7:
            i=[i,month-1]
        else:
            i=[i,month]
        week0.append(i)

    week4=[]
    for i in properweeks[4]:
        if i>=15:
            i=[i,month]
        else:
            i=[i,month+1]
        week4.append(i)

    week5=[]
    for i in properweeks[5]:
        if i>=15:
            i=[i,month]
        else:
            i=[i,month+1]
        week5.append(i)

    week123=[]
    for i in properweeks[1:4]:
        foo=[]
        for x in i:
            x=[x,month]
            foo.append(x)
        week123.append(foo)


    allweeks=[]
    allweeks.append(week0)
    allweeks=allweeks+week123
    allweeks.append(week4)
    allweeks.append(week5)

    return allweeks

@csrf_exempt
def index(request):
    if request.user.is_authenticated:
        x=datetime.datetime.now()
        events=Event.objects.filter(when__range=[f"{int(x.strftime('%Y'))}-{int(x.strftime('%m'))}-{int(x.strftime('%d'))}", f"{int(x.strftime('%Y'))}-{int(x.strftime('%m'))+1}-01"],user=request.user)
        events=events.order_by('when').all()
        if request.method=='PUT':
            data=json.loads(request.body)
            day=data['day']
            month=data['month']
            year=data['year']
            when=datetime.datetime(int(year),int(month),int(day),int(data['from'][:2]),int(data['from'][2:]))
            till=datetime.datetime(int(year),int(month),int(day),int(data['till'][:2]),int(data['till'][2:]))
            newevent=Event.objects.create(user=request.user,eventname=data['eventname'],description=data['description'],when=when,till=till)
            newevent.save()

        
        return render(request, "calender/index.html",{
            'month': x.strftime('%B'),
            'month_id':x.strftime('%m'),
            'weeks': weeks(int(x.strftime('%Y')),int(x.strftime('%m'))),
            'year':x.strftime('%Y'),
            'monthadd1': int(x.strftime('%m'))+1,
            'monthminus1': int(x.strftime('%m'))-1,
            'monthint':int(x.strftime('%m')),
            'events': events
        })
    else:
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
def othermonth(request,year,month):
    if request.user.is_authenticated:
        if month>12:
            month=1
            year+=1
        if month<1:
            month=12
            year-=1

        if request.method=='PUT':
            data=json.loads(request.body)
            day=data['day']
            month=data['month']
            year=data['year']
            when=datetime.datetime(int(year),int(month),int(day),int(data['from'][:2]),int(data['from'][2:]))
            till=datetime.datetime(int(year),int(month),int(day),int(data['till'][:2]),int(data['till'][2:]))
            newevent=Event.objects.create(user=request.user,eventname=data['eventname'],description=data['description'],when=when,till=till)
            newevent.save()

        x=datetime.datetime(year,month,1)
        events=Event.objects.filter(when__range=[f"{int(x.strftime('%Y'))}-{int(x.strftime('%m'))}-{int(x.strftime('%d'))}", f"{int(x.strftime('%Y'))}-{int(x.strftime('%m'))+1}-01"],user=request.user)
        events=events.order_by('when').all()
        return render(request,"calender/othermonth.html",{
            'month': x.strftime('%B'),
            'month_id':x.strftime('%m'),
            'weeks': weeks(int(x.strftime('%Y')),int(x.strftime('%m'))),
            'year':x.strftime('%Y'),
            'monthadd1': int(x.strftime('%m'))+1,
            'monthminus1': int(x.strftime('%m'))-1,
            'monthint':int(x.strftime('%m')),
            'events': events
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def weekview(request):
    if request.user.is_authenticated:
        x=datetime.datetime.now()
        year=int(x.strftime('%Y'))
        month=int(x.strftime('%m'))
        day=int(x.strftime('%d'))
        thisweek=[i for i in weeks(year,month) if [day,month] in i]
        thisweek=thisweek[0]

        y=datetime.datetime(year,thisweek[0][1],thisweek[0][0])
        events=Event.objects.filter(when__range=[y,y+datetime.timedelta(days=6)])

        hours=[]
        for i in range(24):
            for z in range(2):
                if i<10:
                    if len(hours)%2==1:
                        hours.append(f'0{i}30')
                    else:
                        hours.append(f'0{i}00')
                else:
                    if len(hours)%2==1:
                        hours.append(f'{i}30')
                    else:
                        hours.append(f'{i}00')
        return render(request,'calender/weekview.html',{
            'thisweek':thisweek,
            'hours': hours,
            'events':events
        })
    else:
        return HttpResponseRedirect(reverse("login"))
    
def eventapi(request,year,month):
    if request.user.is_authenticated:
        events=Event.objects.filter(when__range=[f"{year}-{month}-01", f"{year}-{int(month)+1}-01"],user=request.user)
        return JsonResponse([event.serailize() for event in events],safe=False)
    else:
        return HttpResponseRedirect(reverse("login"))

def weekeventapi(request):
    if request.user.is_authenticated:
        x=datetime.datetime.now()
        year=int(x.strftime('%Y'))
        month=int(x.strftime('%m'))
        day=int(x.strftime('%d'))
        thisweek=[i for i in weeks(year,month) if [day,month] in i]
        thisweek=thisweek[0]

        y=datetime.datetime(year,thisweek[0][1],thisweek[0][0])
        events=Event.objects.filter(when__range=[y,y+datetime.timedelta(days=7)],user=request.user)
        return JsonResponse([event.serailize() for event in events],safe=False)
    else:
        return HttpResponseRedirect(reverse("login"))    

def editevent(request):
    if request.user.is_authenticated:
        x=datetime.datetime.now()
        events=Event.objects.filter(when__gte=x,user=request.user)
        events=events.order_by('when').all()

        if request.method=='POST' and 'editbutton' in request.POST:
            edit=Event.objects.get(pk=request.POST['editbutton'])
            edit.eventname=request.POST['eventname']
            edit.description=request.POST['description']
            when=datetime.datetime(int(edit.when.strftime('%Y')),int(edit.when.strftime('%m')),int(edit.when.strftime('%d')),int(request.POST['from'][:2]),int(request.POST['from'][2:]))
            till=datetime.datetime(int(edit.till.strftime('%Y')),int(edit.till.strftime('%m')),int(edit.till.strftime('%d')),int(request.POST['till'][:2]),int(request.POST['till'][2:]))
            edit.when=when
            edit.till=till
            edit.save()

        elif request.method=='POST' and 'deletebutton' in request.POST:
            event=Event.objects.get(pk=request.POST['deletebutton'])
            event.delete()

        return render(request, 'calender/editevent.html',{
            'events':events,
        })
    else:
        return HttpResponseRedirect(reverse("login"))    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "calender/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "calender/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "calender/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "calender/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "calender/register.html")