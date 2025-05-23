from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

def portfolio(request):
    return render(
        request, 'portfolio.html'              
    )
    
def login(request):
    return render(
        request, 'user/login.html'              
    )    
    
def regist(request):
    # user_form = UserForm(request.POST or None)
    # if user_form.is_valid():
    #     user = user_form.save(commit=False)
    #     password =user_form.cleaned_data.get('password', '')
    #     try:
    #         validate_password(password)
    #     except ValidationError as e:
    #        user_form.add_error('password', e)
    #        return render(request, 'user/registration.html', context={
    #           'user_form': user_form,   
    #        })
    #     user.set_password(password)
    #     user.save()
    user_form = UserCreationForm(request.POST or None)  
    if user_form.is_valid(): 
        user_form.save()
    return render(request, 'user/registration.html', context={
        'user_form': user_form,   
    })