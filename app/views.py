from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .forms import *
from .models import *
from django.core.mail import send_mail
from django.core import serializers
from django.core.paginator import Paginator

from project.project.settings import STRIPE_PUBLISHABLE_KEY,STRIPE_SECRET_KEY
import stripe

def search_user(username,password,email):
    try:
        name=Users.objects.get(name=username)

    except:
        name=False
    try:
        pwd = Users.objects.get(password=password)
    except:
        pwd = False
    try:
        em = Users.objects.get(email=email)
    except:
        em=False
    return bool(bool(name) + bool(pwd) + bool(em))

def send_conf_message(reciver):
    send_mail(
        'Subject here',
        'Here is the message. http://127.0.0.1:8000/email_conf/%s' %reciver.id,
        'kgevorg97@gmail.com',
        [reciver.email],
        fail_silently=False,
    )


def email_verif(request,r_id):
    user=Users.objects.get(id=r_id)
    user.emailconf=True
    user.save()
    return render(request,'email_conf.html')


def login(request):
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            try:
                user=Users.objects.get(name=form.cleaned_data['name'],
                                   password=form.cleaned_data['password'])
            except :
                form.error='Incorrect username or password'
                return render(request, 'login.html', {'url': 'login', 'form': form})
            if user.emailconf==True:
                request.session['user']=user.id
                request.session.set_expiry(60*60*24*30)

                return render(request,'mine_page.html',{'user':user})

            form.error="Verificate your email"
            return render(request, 'login.html', {'url': 'login', 'form': form})

    elif request.session.has_key('user'):
        user = Users.objects.get(id=request.session['user'])
        return render(request, 'mine_page.html', {'user': user})

    form = NameForm()
    return render(request, 'login.html', {'url': 'login', 'form': form})


def reg(request):
    if request.method == "POST":
        form = RegForm(request.POST)
        if form.is_valid():

            us=search_user(form.cleaned_data['name'],
                        form.cleaned_data['password'],
                        form.cleaned_data['email'])

            if form.cleaned_data['password']==form.cleaned_data['password2'] and us==False:
                user = Users()
                user.name = form.cleaned_data['name']
                user.surname = form.cleaned_data['surname']
                user.email = form.cleaned_data['email']
                user.password = form.cleaned_data['password']
                user.save()
                send_conf_message(user)
                form = RegForm()

                form.message='We send message in yor email'

            else:
                form.error='Passwords is not coincidence'

        return render(request, 'login.html', {'url': 'registration', 'form': form})

    form = RegForm()
    return render(request, 'login.html', {'url': 'registration', 'form': form})

def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST,request.FILES)

        if  form.is_valid():

            product=Products()
            product_ph=Products_photos()

            product.owner=request.session['user']
            product.name=form.cleaned_data['name']

            product.category=form.cleaned_data['category']
            product.info=form.cleaned_data['info']
            product.price=form.cleaned_data['price']
            product.save()

            product_ph.photo_id=product.id
            product_ph.photo = form.cleaned_data['photo']
            product_ph.save()
            return HttpResponse('success <img src="../media/%s">'%product_ph.photo)

    form = AddProductForm()
    return render(request,'add_product.html',{'form':form})


def prod(request,own=None):
    if own==None:
        pr=Products.objects.filter(owner=request.session['user'])
        for i in pr:
            i.photos=[]
            ph=Products_photos.objects.filter(photo_id=i.id)
            for j in ph:
                i.photos.append(j.photo.name)
            i.plist=';'.join(i.photos)
        return render(request,'products.html',{'products':pr})

def basket(request):
    pr=Basket.objects.filter(owner=request.session['user'])
    for i in pr:
        i.photos=[]
        ph=Products_photos.objects.filter(photo_id=i.product.id)
        if (len(ph)!=0):
            i.product.plist=ph[0].photo.name
    return render(request,'basket.html',{'products':pr})


def product(request,own,est=None):
    if request.session.has_key('user'):
        pr=Products.objects.get(id=own)
        if est:
            old_est=pr.rating
            pr.rating=est+old_est
            pr.save()
            return redirect("http://127.0.0.1:8000/product/"+str(own))

        pr.price_to_cent=pr.price*100

        pr.photos=''
        ph=Products_photos.objects.filter(photo_id=pr.id)
        for j in ph:
            pr.photos+= j.photo.name+';'
        status = pr.owner == request.session['user']
        comments=Comments.objects.filter(product=pr)
        return render(request,'product.html',{'product':pr,
                                              'status':status,
                                              'key':STRIPE_PUBLISHABLE_KEY,
                                                'comments':comments})

    return HttpResponse('''<div align='center'><p style="font-size:50px;color:red;">
     Login for mor information </p>
     <a href='/login/'><button>Login</button></a> 
    <a href = '/registration/'><button>Registration </button> </a></div> ''')

def charge(request): # new
    if request.method == 'POST':

        prod_price=int(request.POST['price'])

        stripe.api_key = STRIPE_SECRET_KEY
        charge = stripe.Charge.create(

            amount=prod_price,

            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        return HttpResponse('success',)

def site_home_page(request):
    products=Products.objects.all()
    for i in products:
        i.photos = ''
        ph = Products_photos.objects.filter(photo_id=i.id)

        i.photos+=ph[0].photo.name
    pag_prod=Paginator(products,2)
    pag_prod.page(2)
    return render(request,'site_home_page.html',{'products':products,'pag_prod':pag_prod.page(1)})



def message(request,r_id=None):

    dl=Messages.objects.filter(sender=request.session['user'])
    dl|=Messages.objects.filter(receiver=request.session['user'])

    dllist=[]
    for i in dl:
        us_r=Users.objects.get(id=i.receiver)
        us_s=Users.objects.get(id=i.sender)
        if us_r not in dllist and us_r.id!=request.session['user']:
            dllist.append(us_r)
        if us_s not in dllist and us_s.id!=request.session['user']:
            dllist.append(us_s)
    if request.POST:
        form = Message(request.POST)
        if form.is_valid():
            text=form.cleaned_data['text']
            mes = Messages()
            mes.sender = request.session['user']
            mes.receiver = r_id
            mes.message = text
            mes.save()
            return redirect(request.path)
    form=Message()
    dictionary={'form':form,'r_id':r_id,'dialog':dllist,'user':request.session['user']}
    return render(request,'messages.html',dictionary)

def mess_text(request,r_id):
    if request.is_ajax:
        dltext = Messages.objects.filter(sender=request.session['user'], receiver=r_id)
        dltext |= (Messages.objects.filter(sender=r_id, receiver=request.session['user']))
        dltext=serializers.serialize('json',dltext)
        dltext = JsonResponse({'text': dltext,'user':request.session['user']})
        return dltext

def logout(request):

    del request.session['user']

    return redirect(login)

def comments(request,p_id=None):
    if request.POST and p_id:
        text=request.POST['comment_text']
        newcomm=Comments()
        newcomm.owner=Users.objects.get(id=request.session['user'])
        newcomm.product=Products.objects.get(id=p_id)
        newcomm.comment=text
        newcomm.save()
        return redirect('/product/'+str(p_id))








