
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from App_Login.forms import signupform,UserProfileChange,ProfilePic
def sign_up(requests):
    form = signupform()
    registered = False
    if requests.method == 'POST':
        form = UserCreationForm(data = requests.POST)
        if form.is_valid():
            form.save()
            registered = True
    return render(requests,'App_Login/sign_up.html',{'form':form,'registered':registered})

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

