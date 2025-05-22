from django.shortcuts import render
from django.http import HttpResponse

def portfolio(request):
    return render(
        request, 'portfolio.html'              
    )
    
def login(request):
    return render(
        request, 'users/login.html'              
    )    