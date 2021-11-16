from django.shortcuts import render
from django.http import HttpResponse
from alibaba.forms import UserForm
from django.contrib import messages
from django import forms
from alibaba.models import userinfo,product
from e_com_web.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail
from random import randint
# Create your views here.

def home(r):
    return render(r,'alibaba.html')
    
def signupin(r):
    context = {}
    context["mismatch"] = 0
    return render(r,'signupin.html', context)
    
def sig(r):
    if r.method=='POST':
        em=r.POST.get('email')
        pd = r.POST.get('pd')
        cpd = r.POST.get('cpd')
        if pd and cpd and pd != cpd:
            context = {}
            context["mismatch"] = 1
            context["message"] = 'Password and confirm password is not matching'
            return render(r,'signupin.html', context)
        _mutable = r.POST._mutable
        r.POST._mutable = True
        r.POST.pop('cpd')
        r.POST._mutable = _mutable
        form=UserForm(r.POST)
        if form.is_valid():
            try:
                form.save()
                return render(r,'signupin.html')
            except:
                return HttpResponse('form not saved')
        else:
            form=UserForm()
            context = {}
            context["mismatch"] = 1
            context["message"] = 'provide correct email'
            return render(r,'signupin.html',context)
            
def log_in(r):
    x=0
    u=userinfo.objects.all()
    if(r.method=='POST'):
        email=r.POST['email']
        pd=r.POST['pd']
        for i in u:
            if i.email==email:
                if i.pd==pd:
                    x=1
                    break
        if(x==1):
            return render(r,'alibaba.html')
        else:
            context = {}
            context["mismatch"] = 1
            context["message"] = 'your email or password is incorrect'
            return render(r,'signupin.html',context)
    
def fopd(r):
    return render(r,'fpd.html')
    
def fpd(request):
    if request.method == 'POST':
        email=request.POST['email']
        u=userinfo.objects.all()
        x=0
        for i in u:
            if i.email == email:
                c=i.pd
                x=1
                break
        if(x==0):
            return HttpResponse('you are not a member of alibaba')
        subject = 'alibaba Login Password'
        message = f'Your password is {c}'
        recepient = str(email)
        send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return HttpResponse('check your mail and try again')
    return HttpResponse('there is a problem in our website please try again later')

def detail(r,id):
    context = {'product':product.objects.get(id=id)}
    context['name'] = context['product'].name.split('.')[0]
    context['colors'] = context['product'].color.split('/')
    context['size'] = range(1,13)
    context['c'] = 'c' if context['product'].gender == 'kids ' else ''
    return render(r,'product_page.html', context)
    
    
def add_to_cart(r,id):
    cart = r.session.get('cart')
    if cart:
        quantity = cart.get(id)
        if(quantity != None):
            cart[id] = quantity + 1
        else:
            cart[id] = 1
    else:
        cart = {}
        cart[id] = 1
    r.session['cart'] = cart
    print("\n",cart)
    # return render(r,'add_to_cart.html')
    # return HttpResponse("hue hue hue")
    return open_cart(r)

def open_cart(request):
    cart = request.session.get('cart')
    item_array = []
    total = 0
    ship = 0
    for key in cart:
        if True:
            item = product.objects.get(id = int(key))
            array_item = {}
            name = item.name.split('-')
            array_item['name'] = name[0]
            array_item['subname'] = "-".join(name[1:])
            array_item['image'] = item.image
            array_item['desc'] = item.desc
            array_item['price'] = item.price
            array_item['quantity'] = cart[key]
            ship += cart[key]
            total += int(item.price) * cart[key]
            array_item['code'] = randint(100001,999999)
            item_array.append(array_item)
        # except:
        #     print("error msg")
    print(len(item_array))  
    ship *= 30
    context = {'products':item_array}
    context['subtotal'] = total
    context['shipping'] = ship
    context['total'] = (total+ship)
    return render(request,'add_to_cart.html',context)
    
