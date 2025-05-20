from django.shortcuts import render
from django.http import HttpResponse

def portforlio(request):
    return render(
        request, 'portforlio.html'              
    )