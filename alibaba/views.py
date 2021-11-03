from django.shortcuts import render
from django.http import HttpResponse
from alibaba.forms import UserForm

# Create your views here.

def new(r):
    return HttpResponse('testing')
def signupin(r):
    return render(r,'signupin.html')
def sig(r):
    if r.method=='POST':
        form=UserForm(r.POST)
        if form.is_valid():
            try:
                form.save()
                return render(r,'signupin.html')
            except:
                return HttpResponse('form not saved')
        else:
            form=UserForm()
            return render(r,'signupin.html')
