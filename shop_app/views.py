from django.shortcuts import render, redirect
from shop_app.models import Product, Cart, Order
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.conf import settings    
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages



def to_home(request):
    return redirect('/product/list')

@login_required(login_url='login')
def ProductList(request):
    if request.GET.get('c'):
        category= request.GET.get('c')
        product = Product.objects.filter(category_id=category)
        page_obj=Product.objects.filter(category_id=category)
    else:
        product = Product.objects.all()
        paginator = Paginator(product, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request,'productList.html',{'product':page_obj})



def ProductDetail(request,post_id):
        product=Product.objects.get(id=post_id)
        return render(request,'productDetail.html',{'product':product})

def CartCreate(request, product_id):
    product = Product.objects.get(id=product_id)
    qty_from_request = request.GET.get('qty')
    user = User.objects.get(username='admin')
    if qty_from_request and request.user.id is not None and qty_from_request.isdigit():
        qty = int(qty_from_request)
    else:
        qty = 1
    cart = Cart.objects.create(
        product=product,
        qty=qty,
        user_id=user.id,
        created_at=datetime.now()
    )
    cart.save()
    messages.success(request, f"Added {cart.product.name} successfully.")
    return redirect('/product/list/')

def CartList(request):
    carts = Cart.objects.filter(user_id=request.user.id)
    for item in carts:
        item.total = item.product.price * item.qty
    for item in carts:
        item.save()
    return render(request, 'cartList.html', {'carts': carts})


def CartDelete(request,cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    messages.success(request, f"Deleted {cart.product.name} successfully.")
    return redirect(f'/product/cartList/')


def BuyProduct(request, product_id):
    product = Product.objects.get(id=product_id)
    qty_from_request = request.GET.get('qty')
    
    if qty_from_request is not None and qty_from_request.isdigit():
        product.qty = int(qty_from_request)
        product.total = product.price * product.qty
    else:
        print("Error: Quantity value from request is missing or not a valid integer.")
    if request.method == "GET":
        return render(request, 'orderCreate.html', {'product': product})
    elif request.method == "POST":
        user = request.user
        order = Order.objects.create(
            product=product,  
            user=user,
            total_price=product.total,
            total_qty=product.qty,
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            status='pending',
            created_at=datetime.now()
        )
        messages.success(request, "Order successfully placed.")
        return redirect('/product/list/')
    
def CartOrderCreate(request):
    if request.method == "GET":
        cart = Cart.objects.filter(user_id=request.user.id)
        product = []
        total = 0
        total_qty = 0
        for c in cart:
            product.append({
                'id':c.product.id, 
                'image':c.product.image.url,
                'name':c.product.name, 
                'price':c.product.price, 
                'qty':c.qty, 
                'total':c.product.price * c.qty
                })
            total += c.product.price * c.qty
            total_qty += c.qty
            if request.method=="POST":
                order= Order.objects.create(
                    product = product,
                    user_id = request.user.id,
                    total_price = total,
                    total_qty = total_qty,
                    name = request.POST.get('name'),
                    phone = request.POST.get('phone'),
                    address = request.POST.get('address'),
                    created_at = datetime.now()
                )
    cart.delete()
    messages.success(request, "Order successfully.")
    return redirect(f'/product/list/')


def orderList(request):
    orders = Order.objects.filter(user_id=request.user.id)
    for o in orders:
        o.id = o.id.hex[:8]
    return render(request, 'orderList.html', {'orders': orders})


def orderDelete(request,order_name):
    order = Order.objects.get(name=order_name)
    order.delete()
    messages.success(request, f"Deleted {order.product.name} successfully.")
    return redirect('/product/orderList/') 



def userLogin(request):
    if request.method =="GET":
        return render(request,"login.html") 
    if request.method=="POST":
        username=request.POST.get('name')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Login Successfully')
            return redirect('/product/list')
        else:
            messages.error(request,"Username or password is incorrect")
            return redirect('/login/')
    

def userRegister(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        if request.POST.get('password') == request.POST.get('re_password'):
            try:
                user = User.objects.create(
                    username=request.POST.get('name'),
                    email=request.POST.get('email'),
                    password=make_password(request.POST.get('password'))
                )
                subject = "Hello Welcome"
                html_message = render_to_string('login.html',{'username': user.username}) 
                message = strip_tags(html_message)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['kyawkyaw@gmail.com', ]
                send_mail(subject, message, email_from, recipient_list,html_message=html_message)

                messages.success(request, 'Your account has been registered successfully.')
                return redirect('/login')
            except Exception as e:
                print("Exception occurred during user registration:", e)
                messages.error(request, 'An error occurred while registering your account.')
                return redirect('/register')
        else:   
            messages.error(request, 'Passwords do not match.')
            return redirect('/register')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('/register')



def userLogout(request):
    logout(request)
    messages.success(request,'Logout Successfully')
    return redirect('/login/')


def search_by(request):
    search = request.GET.get('search')
    if search:
        search_terms = search.split() 
        query = Q(name__icontains=search_terms[0])  
        for term in search_terms[1:]:
            query |= Q(name__icontains=term) 
        product = Product.objects.filter(query)
        return render(request, 'productList.html', {'product': product})
    else:
        product = Product.objects.all()
        return render(request, 'productList.html', {'product': product})


