from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
import markdown2
from . import util
from django import forms
from django.urls import reverse
import random


def index(request):
    if request.method=='POST':
        return HttpResponseRedirect(reverse('search'))

    else:        
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def entry(request,title):
    if request.method=='POST':
        return HttpResponseRedirect(reverse('search'))

    if util.get_entry(title)!=None:
        return render(request, "encyclopedia/entry.html", {
            "content": markdown2.markdown(util.get_entry(title)), "title": title
        })
    else:
        return render(request, 'encyclopedia/error.html')

def error(request):
    if request.method=='POST':
        return HttpResponseRedirect(reverse('search'))
        
    return render(request,'encyclopedia/error.html')

def search(request):
    var=request.POST['q']
    lower_var=var.lower()
    lowercase_entry=[x.lower() for x in util.list_entries()]

    if lower_var in lowercase_entry:
        return redirect('entry',title=var)
        
    else:
        potential_search_result=[]
        for i in lowercase_entry:
            if lower_var in i:
                potential_search_result.append(i)

        if len(potential_search_result)>0:
            return render(request, 'encyclopedia/result.html',{
        'search_result':potential_search_result})

        else:
            return HttpResponseRedirect(reverse('error'))

def create(request):
    if request.method=='POST':
        t=request.POST['t']
        c=request.POST['c']
        lowercase_entry=[x.lower() for x in util.list_entries()]
        if t.lower() not in lowercase_entry:
            util.save_entry(t,c)
            return redirect('entry',title=t)
        else:
            return render(request,'encyclopedia/create_error.html',{
                't':t
            })

    else:

        return render(request,'encyclopedia/create.html')

def edit(request,title):
    if request.method=='POST':
        c=request.POST['c']
        util.save_entry(title,c)
        return redirect('entry',title)
    else:
        return render(request,'encyclopedia/edit.html',{ 
            'title':title, "content": util.get_entry(title)
        })

def randompage(request):
    entry_length=len(util.list_entries())
    num1=random.randrange(entry_length)
    t=util.list_entries()[num1]
    return redirect('entry',title=t)
