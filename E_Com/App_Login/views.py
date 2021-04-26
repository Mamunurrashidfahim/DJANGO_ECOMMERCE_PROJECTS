from App_Login.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http.response import HttpResponse, HttpResponseRedirect
from App_Login.forms import ProfileChangeForm, ProfileForm, SignupForm
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def sign_up(request):
    form = SignupForm()

    if request.method =='POST':
        form= SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account Created Successfully!!")
            return HttpResponseRedirect(reverse('App_Login:login'))
    return render(request,'App_Login/sign_up.html',context={'form':form})

def login_user(request):
    form = AuthenticationForm()

    if request.method =='POST':
        form = AuthenticationForm(data= request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('App_Shop:home'))
    return render(request,'App_Login/login.html',context={'form':form})

@login_required
def logout_user(request):
    logout(request)
    messages.warning(request,"You are Logged OUT")
    return HttpResponseRedirect(reverse('App_Shop:home'))


@login_required
def user_profile(request):
    profile = Profile.objects.get(user = request.user)
    form = ProfileForm(instance=profile)
    if request.method =='POST':
        form=ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Change Saved!!")
            form = ProfileForm(instance=profile)
    return render(request,'App_Login/change_profile.html',context={'form':form})


@login_required
def user_change(request):
    current_user = request.user
    form = ProfileChangeForm(instance=current_user)
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request,"Email Change Successfully!!")
            form = ProfileChangeForm(instance=current_user)
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/edit_user.html', context={'form': form})


@login_required
def pass_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Password Change Successfully!!")
            return HttpResponseRedirect(reverse('App_Login:profile'))
            changed = True
    return render(request, 'App_Login/pass_change.html', context={'form': form, 'changed': changed})