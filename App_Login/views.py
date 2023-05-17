
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from django.conf import settings
import uuid
from django.core.mail import send_mail
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from App_Login.forms import signupform,UserProfileChange,ProfilePic
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  


def sign_up(requests):
    
    
    if requests.method == 'POST':
        form = signupform(requests.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            emailvalue= form.cleaned_data.get("email")
            passwordvalue1= form.cleaned_data.get("password1")
            passwordvalue2= form.cleaned_data.get("password2")
            user = form.save(commit=False)  
            if passwordvalue1 == passwordvalue2:
                try:
                    user= User.objects.get(email=emailvalue)
                    messages.success(requests,"The email you entered has already been taken. Please try another email.")
                    return render(requests,'App_Login/sign_up.html',{'form':form})
                except User.DoesNotExist:
                    user.is_active = False  
                    user.save()  
                    # to get the domain of the current site  
                    current_site = get_current_site(requests)  
                    mail_subject = 'Blog Account Verification '  
                    message = render_to_string('App_Login/acc_active_email.html', {  
                        'user': user,  
                        'domain': current_site.domain,  
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                        'token':account_activation_token.make_token(user),  
                    })  
                    to_email = form.cleaned_data.get('email')  
                    email = EmailMessage(  
                                mail_subject, message, to=[to_email]  
                    )  
                    email.send()  
                    messages.success(requests,"Please confirm your email address to complete the registration.")
            else:
                messages.success(requests,"The email you entered has already been taken. Please try another email.")
                return render(requests,'App_Login/sign_up.html',{'form':form})
            
    else:
        form = signupform()  
           
             
    return render(requests,'App_Login/sign_up.html',{'form':form})

def login_page(requests):
    form = AuthenticationForm()
    if requests.method == "POST":
        form = AuthenticationForm(data = requests.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(requests,user)
                return HttpResponseRedirect(reverse('home'))
    return render(requests,'App_Login/login.html',{'form':form})

@login_required
def logout_user(requests):
    logout(requests)
    return HttpResponseRedirect(reverse('login'))

@login_required
def profile(requests):
    return  render(requests,'App_Login/profile.html')

@login_required
def user_change(requests):
    current_user  = requests.user
    form = UserProfileChange(instance = current_user)
    if requests.method =="POST":
        form = UserProfileChange(requests.POST,instance = current_user)
        if form.is_valid:
            form.save()
            form = UserProfileChange(instance = current_user)
    return render(requests,'App_Login/change_profile.html',{'form':form})

@login_required
def pass_change(requests):
    current_user = requests.user
    changed = False
    form = PasswordChangeForm(current_user)
    if requests.method == "POST":
        form = PasswordChangeForm(current_user,data =requests.POST)
        if form.is_valid():
            form.save()
            changed = True
    return render(requests,"App_Login/passchange.html",{'form':form,'changed':changed})

@login_required
def add_pro_pic(requests):
    form = ProfilePic()
    if requests.method =="POST":
        form = ProfilePic(requests.POST,requests.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = requests.user
            user_obj.save()
            return HttpResponseRedirect(reverse('profile'))
    return render(requests,"App_Login/pro_pic_add.html",{'form':form})


@login_required
def change_pro_pic(requests):
    form = ProfilePic()
    form = ProfilePic(instance=requests.user.user_profile)
    if requests.method=="POST":
        form = ProfilePic(requests.POST,requests.FILES,instance=requests.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
    return render(requests,"App_Login/pro_pic_add.html",{'form':form})


def error(requests):
    return render(requests,'App_Login/error.html')

def activate(request, uidb64, token):  
    User = get_user_model()  
    valid = False
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        valid = True
        return render(request,"App_Login/success.html",{'valid':valid})  
    else:  
        return render(request,"App_Login/success.html",{'valid':valid})    