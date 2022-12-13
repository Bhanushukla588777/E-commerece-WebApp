from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import datetime
from django.db import connection
# Create your views here.

def home(request):

    cdata = category.objects.all().order_by('id')[0:6]
    pdata = products.objects.all().order_by('id')[0:70]
    noofitemsincart=addtocart.objects.all().count()
    print(noofitemsincart)
    return render(request,'user/index.html',{"data":cdata,"prod":pdata,"noofitemsincart":noofitemsincart})


def about(request):
    return render(request,'user/about.html')

def contactus(request):
    status=False
    if request.method=='POST':
        Name = request.POST.get("name", "")
        Email = request.POST.get("email", "")
        Mobile = request.POST.get("mobile", "")
        Message = request.POST.get("message", "")
        x=contact(name=Name, email=Email, mobile=Mobile, message=Message)
        x.save()
        status= True
    return render(request, 'user/contactus.html', {'S':status})

def services(request):
    return render(request,'user/services.html')

def myorders(request):
    userid=request.session.get('userid')
    oid=request.GET.get('oid')
    orderdata=""
    if userid:
        cursor=connection.cursor()
        cursor.execute("select o.*,p.* from user_order o,user_products p where o.pid=p.id and o.userid='"+str()+"'")
        orderdata=cursor.fetchall()
        if oid:
            result=order.objects.filter(id=oid,userid=userid)
            result.delete()
            return HttpResponse("<script>alert('Your Order Has Been Cancelled...');window.location.href='/user/myorders'</script>")

    return render(request, 'user/myorders.html',{"pendingorder":orderdata})

def myprofile(request):
    user=request.session.get('userid')
    pdata=signup.objects.filter(email=user)
    if user:
        if request.method == 'POST':
            name = request.POST.get("name", "")
            father = request.POST.get("father", "")
            mother = request.POST.get("mother", "")
            dob = request.POST.get("dob", "")
            contact = request.POST.get("contact", "")
            password = request.POST.get("passwd", "")
            address = request.POST.get("address", "")
            picname = request.FILES['fu']
            signup(email=user,name=name,father=father,mother=mother,dob=dob,contact=contact,passwd=password,ppic=picname,address=address).save()
            return HttpResponse("<script>alert('Your  Profile Updated Succesfully..');window.location.href='/user/myprofile/';</script>")
    return render(request, 'user/myprofile.html',{"signup":pdata})


def product(request):
    cdata = category.objects.all().order_by('id')
    x = request.GET.get('abc')
    if x is not None:
        pdata = products.objects.filter(category=x)
    else:
        pdata = products.objects.all().order_by('id')

    return render(request, 'user/product.html', {"cat":cdata,"prod":pdata})

def signup_reg(request):
    if request.method=='POST':
        name = request.POST.get("name","")
        father = request.POST.get("father","")
        mother = request.POST.get("mother", "")
        email = request.POST.get("email","")
        dob = request.POST.get("dob","")
        contact = request.POST.get("contact","")
        password = request.POST.get("passwd","")
        address = request.POST.get("address", "")
        picname = request.FILES['fu']
        d=signup.objects.filter(email=email)

        if d.count()>0:
            return HttpResponse("<script>alert('You Are already Registered...');window.location.href='/user/signup';</script>")
        else:
            signup(name=name, father=father, mother=mother, email=email,dob=dob, contact=contact, passwd=password, address=address, ppic=picname).save()
            return HttpResponse("<script>alert('Your Registration Are Successfully...');window.location.href='/user/signup';</script>")


    return render(request, 'user/signup.html')


def login(request):
    if request.method=='POST':

        email = request.POST.get("email","")
        passwd = request.POST.get("passwd","")
        checkuser =signup.objects.filter(email=email,passwd=passwd)
        if(checkuser):
           request.session['userid']=email
           return HttpResponse("<script>alert('Login Successfully...');window.location.href='/user/signin';</script>")
        else:
            return HttpResponse("<script>alert('User id and Password is Incorrect...');window.location.href='/user/signin';</script>")
    return render(request,'user/signin.html')

def prodetails(request):
    a = request.GET.get('msg')
    pdata = products.objects.filter(id=a)

    return render(request,'user/prodetails.html', {"d":pdata})

def process(request):
    userid =request.session.get('userid')
    pid=request.GET.get('pid')
    btn=request.GET.get('bn')
    print(userid,pid,btn)
    if userid is not None:
        if btn=='cart':
           checkcartitem=addtocart.objects.filter(pid=pid,userid=userid)
           if checkcartitem.count()  == 0:
                addtocart(pid=pid,userid=userid,status=True,cdate=datetime.datetime.now()).save()
           else:
               return HttpResponse("<script>alert('This item is already added in cart...');window.location.href='/user/home/'</script>")
        elif  btn=='order':
            order(pid=pid,userid=userid,remarks="pending",status=True,odate=datetime.datetime.now()).save()
            return HttpResponse("<script>alert('Your Order Have Confirmed....');window.location.href='/user/myorders/'</script>")

        elif btn== 'orderfromcart':
            res=addtocart.objects.filter(pid=pid,userid=userid)
            res.delete()
            order(pid=pid,userid=userid,remarks="Pending",status=True,odate=datetime.datetime.now()).save()
            return HttpResponse("<script>alert('Your Order Have Confirmed....');window.location.href='/user/myorders/'</script>")
        return render(request, 'user/process.html', {"alreadylogin": True})

    else:
        return HttpResponse("<script>window.location.href='/user/signin/'</script>")

def logout(request):
    del request.session['userid']
    return HttpResponse("<script>window.location.href='/user/home/'</script>")

def cart(request):
    if request.session.get('userid'):
        userid=request.session.get('userid')
        cursor=connection.cursor()
        cursor.execute("select c.*,p.* from  user_addtocart c,user_products p where p.id=c.pid and userid='"+str(userid)+"'")
        cartdata=cursor.fetchall()
        pid=request.GET.get('pid')
        if request.GET.get('pid'):
           res=addtocart.objects.filter(id=pid,userid=userid)
           res.delete()
           return HttpResponse("<script>alert('Your Product Item Has Been Removed Successfully....');window.location.href='/user/cart/'</script>")
    return render(request,'user/cart.html',{"cart": cartdata})
