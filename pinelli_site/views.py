from django.shortcuts import render, redirect
from django.http import HttpResponse #HttpResponse-> metatrepei ta keimena se html
from .models import Product
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
import json

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
    product_by_id=Product.objects.get(id=id)#i take from my database the id that the URL has    
    return render(request,"product.html",{"product":product_by_id})

def addproduct(request):
    if request.method == 'POST':
        title=request.POST["title"]
        price=request.POST["price"]
        description=request.POST["description"]
        category=request.POST["category"]
        sub_category=request.POST["sub_category"]
        indoors=request.POST["indoors"]
        image=request.POST["image"]
    elif request.method == 'GET':
        return render(request,"addproduct.html")

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
    print ("cc", product_id)
    print(cart)
    if str(product_id) in cart.keys():
        cart.pop(str(product_id))
        print(cart)
    request.session['cart'] = cart
    return redirect('cart_view')

def checkout(request):
    request.session['cart'] = {}
    return render(request, 'checkout.html', {'message': 'Thank you for your purchase!'})

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

