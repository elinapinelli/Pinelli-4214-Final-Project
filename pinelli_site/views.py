from django.shortcuts import render
from django.http import HttpResponse #HttpResponse-> metatrepei ta keimena se html
from .models import Product
from django.db.models import Q

# Create your views here.

def home(request):#sinartisi pou servirei tin kentriki selida tou site
    return render(request,"home.html")

def about(request):#sinartisi pou servirei tin kentriki selida tou site
    return render(request,"about.html")

def products(request):#sinartisi pou servirei tin products selida tou site
    product_list=Product.objects.all()#pairno ta products apo database
    return render(request,"products.html",{"products":product_list})

def product(request,id):#sinartisi pou servirei tin products selida tou site
    product_by_id=Product.objects.get(id=id)#i take from my database the id that the URL has
    return render(request,"product.html",{"product":product_by_id})

def search(request):#sinartisi pou servirei tin products selida tou site
    # if the user search a word that includes indoors or outdoors it will search for True or False otherwise if the title, description, category and sub category contains the keyword 
    keyword=request.POST["keyword"]
    if "indoors".find(keyword)>-1:
        product_list=Product.objects.filter(indoors=True)    
    elif "outdoors".find(keyword)>-1:
        product_list=Product.objects.filter(indoors=False)  
    else:
        product_list=Product.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(category__icontains=keyword) | Q(sub_category__icontains=keyword) )
    return render(request,"products.html",{"products":product_list})