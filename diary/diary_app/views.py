from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

def portfolio(request):
    return render(
        request, 'portfolio.html'              
    )
    
def home(request):
    return render(
        request, 'home.html'
    )    
    
def login(request):
    return render(
        request, 'user/login.html'              
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
    pass    
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
   