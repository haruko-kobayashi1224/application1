from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import UserActivateToken
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 

def portfolio(request):
    return render(
        request, 'portfolio.html'              
    )
    
    
def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
       regist_form.save(commit=True)
       return redirect('diary_app:home')
    return render(
        request, 'user/registration.html', context={
            'regist_form': regist_form,   
        }
    )
def activate_user(request, token):
    activate_form = forms.UserActivateForm(request.POST or None)
    if activate_form.is_valid():
        UserActivateToken.objects.activate_user_by_token(token) #ユーザーを有効化
        messages.success(request,'ユーザーを有効化しました')
    activate_form.initial['token'] = token
    return render(
        request, 'user/activate_user.html', context={
            'activate_form': activate_form,
        }
    )  
    
def user_login(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data['email']
        password =login_form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('diary_app:home')
        else:
            messages.warning(request, 'ログインに失敗しました')
    return render(
        request, 'user/user_login.html', context={
            'login_form': login_form,
        }              
    )    
@login_required    
def user_logout(request):    
    logout(request)    
    return redirect('diary_app:user_login')
    #     password =user_form.cleaned_data.get('password', '')
    #     try:
    #         validate_password(password)
    #     except ValidationError as e:
    #        user_form.add_error('password', e)
    #     user.set_password(password)
    #     user.save()
    # user_form = UserCreationForm(request.POST or None)  
    # if user_form.is_valid(): 
    #     user_form.save()
    
def home(request):
    return render(
        request, 'home.html'
    )   
        
def today_diary(request):
    return render(
        request, 'today_diary.html'
    )   

def reflection(request):
    return render(
        request, 'reflection.html'
    )    
    
def my_page(request):
    return render(
        request, 'my_page.html'
    )    
             
       