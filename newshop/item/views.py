from email import message
from django.contrib import messages
import json
from tkinter.tix import Tree
from django.shortcuts import render, redirect 
import _json
from itertools import product
from unicodedata import category, name
from requests.adapters import HTTPAdapter
from django.http import request ,JsonResponse
from django.shortcuts import get_object_or_404, render
from item.models import *
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import *
from .utils import *

def allprod(request,c_slug=None):
    c_name=None
    catitem=None
    proditem=None  
    if c_slug == None:
        catitem= Category.objects.all()

        p = Paginator( catitem, 2 )
        pageno = request.GET.get('page', 1)

        try:
            cat = p.page(pageno)
        except EmptyPage :
            cat = p.page(1)
        
    else:
        c_name=get_object_or_404(Category,slug=c_slug) 
        # c_name=Category.objects.get(slug=c_slug) #another method 
        
        # the above command get object is used to retrieve a particular instance using a uniques value like slug or id
        proditem= Product.objects.filter(category=c_name,available=True) 
        # in above line c_name refered by the instance 's name
        
        p = Paginator( proditem, 2 )
        pageno = request.GET.get('page', 1)
        
        try:
            cat = p.page(pageno)
        except EmptyPage:
            cat = p.page(1)
        
    return render(request,'index.html',{'catitem':catitem,'proditem':proditem,'c_name':c_name,'cat':cat,})


def proddesc(request,p_slug):
    product=get_object_or_404(Product,slug=p_slug)
    messages.info(request,'Item added to cart')
    return render(request,'product.html',{'product':product})


def search(request):        
    searchitem = None
    product = None

    if request.method == "POST":
        searchitem = request.POST['searchitem']
        product = Product.objects.filter(name__contains = searchitem)        

    return render(request,'searchresult.html',{'products':product,'searchitem':searchitem})

def update_item(request):
    data = json.loads(request.body)
    productId= data['productId']
    action= data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer      
    product = Product.objects.get(id = productId)  
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem, created= OrderItem.objects.get_or_create(order=order, product=product)

    if action=='add':
        orderitem.quantity = (orderitem.quantity +1)

    elif action=='remove':
        orderitem.quantity = (orderitem.quantity -1)

    orderitem.save()

    if orderitem.quantity <= 0 :
        orderitem.delete()  


    return JsonResponse('Item was added', safe=False)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    
    else:
        cookiedata = cookieCart(request)
        cartitems = cookiedata['cartItems']
        order = cookiedata['order']
        items = cookiedata['items']        
        
    return render(request,'cart.html',{'items':items,'order':order,'cartitems':cartitems})

# def update_address(request):    
#     if request.user.is_authenticated:
#         physical = None
#         update=True
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer,complete=False)
#         items = order.orderitem_set.all()
#         address = ShippingAddress.objects.get(customer=customer, order = order)                 

            
#     return render(request,'checkout.html',{'order':order,'update':update})


def checkout(request,updation=None):    
    
    if request.user.is_authenticated:        
        update_required = updation
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        add = ShippingAddress.objects.get(customer=customer, order = order)

        if request.method == 'POST':                                     
            addr = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zipcode = request.POST['zipcode']
            add.address= addr
            add.city= city
            add.state= state
            add.zipcode= zipcode
            add.save()
        
            
    else:     
        add=None # since it was showing add reference before assignment 
        update_required = False
        cookiedata = cookieCart(request)
        cartitems = cookiedata['cartItems']
        order = cookiedata['order']
        items = cookiedata['items']        

    return render(request,'checkout.html',{'cartitems':cartitems,'items':items,'order':order,'add':add,'update_required':update_required})

    # for item in items:
    #     if item.product.digital == False:
    #         physical = True
    #         break 
    
    # address = ShippingAddress.objects.get(customer=customer, order = order)


    

    #     # cus1 = Customer.objects.get(id=2)
    #     # order = cus1.order_set.all()



# the below is the method shown in video session
# def allprod(request,c_slug=None):
#     c_page=None 
#     products=None 
#     if c_slug!=None:
#         c_page=get_object_or_404(Category,slug=c_slug)
#         products=Product.objects.all().filter(category=c_page,available=True)
#     else:
#         products=Product.objects.all().filter(available=True)
    
#     return render(request,'base.html',{'category':c_page,'product':products})

