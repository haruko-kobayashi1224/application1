from django.shortcuts import render
from .forms import UserForm
def portfolio(request):
    return render(
        request, 'portfolio.html'              
    )
    
def login(request):
    return render(
        request, 'user/login.html'              
    )    
    
def regist(request):
    user_form = UserForm(request.POST or None)
    return render(request, 'user/registration.html', context={
        'user_form': user_form,   
    })