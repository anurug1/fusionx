
# from django.contrib.auth import authenticate,login,logout
from msilib.schema import ListView
from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
from .models import *
# from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib import messages
import json
import datetime
from .utils import cookieCart,cartData,guestOrder
from django.contrib.auth.decorators import login_required

def index(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    
    products = Product.objects.all()    
    context = {'navbar':'index','products':products,'cartItems':cartItems,'order':order}
    return render(request,"index.html",context)

def shop(request):
    brands = Brand.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    products = Product.objects.filter(published=True)
    
    brid = request.GET.get('brandid')
    print(brid)
    if brid:
        products = products.filter(brand_id=brid)
        
    paginator = Paginator(products,6)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
        
    
    context = {'navbar':'shop','products':products,'cartItems':cartItems,'order':order,'brands':brands}
    return render(request,"shop.html",context)

def about(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    context = {'navbar':'about','cartItems':cartItems,'order':order}
    return render(request,"about.html",context)

def productdetails(request,id):

    product = Product.objects.get(id=id)  
    sizes = Size.objects.all()
    # product = get_object_or_404(Product,id)
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'navbar':'shop',"product":product,'items':items,'order':order,'cartItems':cartItems,"sizes":sizes}
    return render(request,"shop-details.html",context)

# @login_required(login_url="login")
def shoppingcart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'navbar':'page','items':items,'order':order,'cartItems':cartItems}
    return render(request,"shopping-cart.html",context)

# @login_required(login_url="login")
def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'navbar':'page','items':items,'order':order,'cartItems':cartItems}
    return render(request,"checkout.html",context)

# @login_required(login_url="login")
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action:', action)
    print('Product:', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem , created = OrderItem.objects.get_or_create(order=order,product=product)
    
    if action =='add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)
    elif action == 'delete':
        orderItem.quantity = (orderItem.quantity -500)
    
    orderItem.save()
    
    if orderItem.quantity <=0:
        orderItem.delete()
        
    return JsonResponse('Item was added',safe=False)

# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
    else:
        customer,order = guestOrder(request,data)
            
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping == True:
            ShippingAddress.objects.create(
                    customer = customer,
                    order = order,
                    address = data['shipping']['address'],
                    country = data['shipping']['country'],
                    city = data['shipping']['city'],
                    state = data['shipping']['state'],
                    zipcode = data['shipping']['zipcode'],
                    phone = data['shipping']['phone'],
        )
    return JsonResponse('Payment complete!',safe=False)