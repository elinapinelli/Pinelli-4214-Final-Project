from django.shortcuts import render
from django.http import HttpResponse #HttpResponse-> metatrepei ta keimena se html

# Create your views here.

def home(request):#sinartisi pou servirei tin kentriki selida tou site
    return render(request,"home.html")

def about(request):#sinartisi pou servirei tin kentriki selida tou site
    return render(request,"about.html")