from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse #HttpResponse-> metatrepei ta keimena se html
from .models import Product,Rating
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
import json
from django.conf import settings
import os
from django.contrib import messages

# Create your views here.

def home(request):#sinartisi pou servirei tin kentriki selida tou site
    return render(request,"home.html")

def about(request):#sinartisi pou servirei tin kentriki selida tou site
    return render(request,"about.html")

def products(request):#sinartisi pou servirei tin products selida tou site
    product_list=Product.objects.all()#pairno ta products apo database
    
    # I convert the data of the products from django to the list in order to pass to javascript
    products=[{"id":product.id,"title":product.title,"price":product.price,"description":product.description,"category":product.category, "sub_category":product.sub_category, "indoors": product.indoors, "image": product.image.url } for product in product_list]
    
    #i give them to html and json.dumps converts the list to string
    return render(request,"products.html",{"products":product_list,"products_str":json.dumps(products)})

def product(request,id):#sinartisi pou servirei tin products selida tou site
    if request.method == 'POST':
        product_by_id=Product.objects.get(id=id)#get product by id
        product_by_id.delete()
        messages.success(request,f"Product ({product_by_id.title}) deleted successfully")
        return redirect("products")

    if request.method == 'GET':
        product_by_id=Product.objects.get(id=id)#i take from my database the id that the URL has    
        return render(request,"product.html",{"product":product_by_id})

def addproduct(request):
    if request.method == 'POST':
        title=request.POST["title"]
        price=request.POST["price"]
        description=request.POST["description"]
        category=request.POST["category"].capitalize()#i capitalized the first letter it because if it is not capitalized it will make a new category
        sub_category=request.POST["sub_category"].capitalize()
        try:
            indoors=request.POST["indoors"]#i try to take the ckecked indoors and if the user doesnt click it i take it as false
            if indoors=="":
                indoors=True
        except:
            indoors=False
        image=request.FILES["image"]#because it is an file i take it from FILES
        upload_folder = os.path.join(settings.BASE_DIR, 'static\images')#the folder i will save it
        file_path=os.path.join(upload_folder,image.name)#where it will save it
        if not os.path.exists(upload_folder):#if the folder doesnt exist create one in order to not have errors
            os.makedirs(upload_folder)
        with open(file_path, 'wb+') as destination: #i save the file using chunks that posted because the form i made send chunks
            for chunk in image.chunks():
                destination.write(chunk)
        Product.objects.create(title=title,price=price,description=description,indoors=indoors,category=category,sub_category=sub_category,image="static/images/"+image.name)
        messages.success(request,f"You add a product ({title}) successfully")
        return  render(request,"addproduct.html")

    elif request.method == 'GET':
        return render(request,"addproduct.html")

def updateproduct(request,product_id):
    product_by_id=Product.objects.get(id=product_id)#get product by id
    if request.method == 'POST':
        title=request.POST["title"]
        price=request.POST["price"]
        description=request.POST["description"]
        category=request.POST["category"].capitalize()#i capitalized the first letter it because if it is not capitalized it will make a new category
        sub_category=request.POST["sub_category"].capitalize()
        try:
            indoors=request.POST["indoors"]#i try to take the ckecked indoors and if the user doesnt click it i take it as false
            if indoors=="":
                indoors=True
        except:
            indoors=False
        try:    
            image=request.FILES["image"]#because it is an file i take it from FILES
        except:
            image=None   
        if image!=None:     
            upload_folder = os.path.join(settings.BASE_DIR, 'static\images')#the folder i will save it
            file_path=os.path.join(upload_folder,image.name)#where it will save it
            if not os.path.exists(upload_folder):#if the folder doesnt exist create one in order to not have errors
                os.makedirs(upload_folder)
            with open(file_path, 'wb+') as destination: #i save the file using chunks that posted because the form i made send chunks
                for chunk in image.chunks():
                    destination.write(chunk)
        print(title,indoors)
        product_by_id.title=title
        product_by_id.price=price
        product_by_id.description=description
        product_by_id.category=category
        product_by_id.sub_category=sub_category
        product_by_id.indoors=indoors
        if image!=None:
            product_by_id.image="static/images/"+image.name
        product_by_id.save()    
        messages.success(request, f'Product ({title}) update successfully !!')
        return redirect("products")
    elif request.method == 'GET':
       
        # print(product_by_id)
        return  render(request,"addproduct.html",{"product":product_by_id})

def search(request):#sinartisi pou servirei tin products selida tou site
    # if the user search a word that includes indoors or outdoors it will search for True or False otherwise if the title, description, category and sub category contains the keyword 
    keyword=request.POST["keyword"]
    if "indoors".find(keyword)>-1:
        product_list=Product.objects.filter(indoors=True)    
    elif "outdoors".find(keyword)>-1:
        product_list=Product.objects.filter(indoors=False)  
    else:
        product_list=Product.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(category__icontains=keyword) | Q(sub_category__icontains=keyword) )
    # I convert the data of the products from django to the list in order to pass to javascript
    products=[{"id":product.id,"title":product.title,"price":product.price,"description":product.description,"category":product.category, "sub_category":product.sub_category, "indoors": product.indoors, "image": product.image.url } for product in product_list]
    
    return render(request,"products.html",{"products":product_list,"products_str":json.dumps(products)})

def order(request):#sinartisi pou servirei tin kentriki selida tou site
    return render(request,"order.html")

def add_to_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    request.session['cart'] = cart
    return redirect('cart_view')



def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    total_quantity = 0  # To store the total quantity of all products

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity,  # Total price for this item
        })
        total_price += product.price * quantity
        total_quantity += quantity  # Add the quantity of this product to total quantity

    return render(request, 'order.html', {
        'cart': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,  # Passing total quantity to the template
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart.keys():
        cart.pop(str(product_id))     
    request.session['cart'] = cart
    return redirect('cart_view')

def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity,  # Total price for this item
        })
        total_price += product.price * quantity

    if request.method == 'POST':
        street = request.POST.get('street')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        # Add basic validation
        if not (street and city and zip_code and card_number and expiry_date and cvv):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('checkout')

        # Simulate successful payment
        request.session['cart'] = {}  # Clear the cart
        messages.success(request, 'Thank you for your purchase!')
        return redirect('home')

    return render(request, 'checkout.html', {
        'cart': cart_items,
        'total_price': total_price,
    })
@login_required
def profile(request):
    # Display the user's profile
    return render(request, 'profile.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after saving
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

def rating(request):
   
    if request.method == 'POST':
        data = json.loads(request.body)
        username=data["username"]
        rating=data["rating"]
        product_id=data["product_id"]
        print(username,rating,product_id)
        Rating.objects.create(username=username,rating=rating,product_id=product_id)
        return JsonResponse({"status":"success"}, content_type="application/json")

