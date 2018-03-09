from django.shortcuts import render,HttpResponse,redirect
from django.conf.urls import url

# Create your views here.

def index(request):
    return HttpResponse('hello world')




urlpatterns = [

    url('',index)

]