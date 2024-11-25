from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as django_login,logout as django_logout
from django.contrib import messages

# Create your views here.
def login(request):#sinartisi pou servirei tin kentriki selida tou site
    if request.method=="POST":
        #I take the data from POST
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:#an ta stoixeia pou postare o user einai sosta
            django_login(request,user)
            messages.success(request,f"Welcome {username}")
            return redirect("/")
        else:
            messages.error(request,"Invalid username or password")
            return redirect("/accounts/login")

    elif request.method=="GET":
        return render(request,"login.html")

def register(request):#sinartisi pou servirei tin kentriki selida tou site
    if request.method=="POST": 
        #I take the data from POST
        username=request.POST["username"]
        password=request.POST["password"]
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        email=request.POST["email"]
        if User.objects.filter(username=username).exists():#iparxei idi to username
            messages.error(request,"username already exists.")
            return redirect("/accounts/register")
        elif User.objects.filter(email=email).exists():
            messages.error(request,"email already exists.")
            return redirect("/accounts/register")
        else:#ola pigan kala ton grafoume stin database
            user=User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)   
            user.save()
            messages.success(request,f"User created succesfully with username : {username}")
            return redirect("/accounts/login")

    elif request.method=="GET":
        return render(request,"register.html")

def logout(request):#sinartisi pou servirei tin kentriki selida tou site
    messages.success(request,f"{request.user.username} logout sucessfully")
    django_logout(request)
    return redirect("/")

