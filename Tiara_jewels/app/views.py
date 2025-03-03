from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from . models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
# from django.shortcuts import render,redirect,get_object_or_404

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.conf import settings
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
# from django.utils import timezone
# Create your views here.

def shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        data=authenticate(username=uname,password=password)
        if data:
            login(req,data)
            if data.is_superuser:
                req.session['shop']=uname
                return redirect(shop_home)
            else:
                req.session['user']=uname
                # return redirect(user_home)
        else:
            messages.warning(req,"invalid user or password")  
        return redirect(shop_login)
    else:      
        return render(req,'login.html')
    
def shop_logout(req):
    logout(req)
    req.session.flush()
    return redirect(shop_login)



def register(req):
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        password = req.POST['password']
        
        if not name or not email or not password:
            messages.warning(req, "All fields are required.")
            return redirect(register)
        
        try:
            EmailValidator()(email)
        except ValidationError:
            messages.warning(req, "Please enter a valid email address.")
            return redirect(register)
        
        if len(password) < 8:
            messages.warning(req, "Password must be at least 8 characters long.")
            return redirect(register)

        if User.objects.filter(email=email).exists():
            messages.warning(req, "User with this email already exists.")
            return redirect(register)

        try:
            # Create the user
            data = User.objects.create_user(first_name=name, username=email, email=email, password=password)
            data.save()

            # Send confirmation email
            subject = 'Registration Successful'
            message = f'Hello {name},\n\nThank you for registering on our platform.\n\nBest regards,\nYour Company Name'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            send_mail(subject, message, from_email, recipient_list)

            messages.success(req, "Registration successful! A confirmation email has been sent.")
            return redirect(shop_login)  # Assuming shop_login is the login view

        except Exception as e:
            # Catch unexpected errors
            messages.warning(req, f"Error: {str(e)}")
            return redirect(register)

    else:
        return render(req, 'register.html')
    
# def public(req):
#     return render(req,'public.html')

    

 #------------------------------admin------------------------------------------------------------------------------------------



def shop_home(req):
    if 'shop' in req.session:
        products=Jewelry.objects.all()
        return render(req,'shop/shop_home.html',{'jewels':products})
        # return render(req,'shop/shop_home.html')
    else:
        return redirect(shop_login) 
    
def add_product(req):
    if req.method=='POST':
        name=req.POST['name']
        description=req.POST['description']
        material=req.POST['material']
        price=req.POST['price']
        weight=req.POST['weight']
        category_name = req.POST.get('JewelryType')
        file=req.FILES['img']

        try:
            category = JewelryType.objects.get(name=category_name)
        except JewelryType.DoesNotExist:
            messages.error(req, "Category does not exist!")
            return redirect('add_pro')  
        data= Jewelry.objects.create(name=name,description=description,material=material,price=price,weight=weight,image=file,category=category)
        data.save()
        return redirect(shop_home)
    return render(req,'shop/add_pro.html')   

def edit_pro(req,id):
    pro=Jewelry.objects.get(pk=id)
    if req.method=='POST':
        name=req.POST['name']
        description=req.POST['description']
        material=req.POST['material']
        price=req.POST['price']
        weight=req.POST['weight']
        # category_name = req.POST.get('JewelryType')
        file=req.FILES['img']  
        if file:
            Jewelry.objects.filter(pk=id).update(name=name,description=description,material=material,price=price,weight=weight)
        else:
            Jewelry.objects.filter(pk=id).update(name=name,description=description,material=material,price=price,weight=weight)
        
        return redirect(ring_page)
    return render(req,'shop/edit_pro.html',{'data':pro})

def bookings(req):
    bookings = Buy.objects.all().order_by('-date')  
    user_addresses = Address.objects.filter(user=req.user)
    print(f"User: {req.user}") 
    print(f"User Addresses: {user_addresses}") 
    # Return the data to the template
    return render(req, 'shop/booking.html', {'data': bookings, 'user_addresses': user_addresses})




def delete_pro(req,id):
    data=Jewelry.objects.get(pk=id)
    url=data.image.url
    url=url.split('/')[-1]
    os.remove('media/'+url)
    data.delete()
    return redirect(ring_page)


#  displaying all Rings
def ring_page(request):
    ring_category = JewelryType.objects.get(name='ring') 
    rings = Jewelry.objects.filter(category=ring_category)
    return render(request, 'shop/ring_page.html', {'jewelry_items': rings})

#  displaying all Necklaces
def necklace_page(request):
    necklace_category = JewelryType.objects.get(name='necklace')
    necklaces = Jewelry.objects.filter(category=necklace_category)
    return render(request, 'shop/ring_page.html', {'jewelry_items': necklaces})

def earrings_page(request):
    earrings_category = JewelryType.objects.get(name='earrings')
    earrings = Jewelry.objects.filter(category=earrings_category)
    return render(request, 'shop/ring_page.html', {'jewelry_items': earrings })

def Bracelet_page(request):
    Bracelet_category = JewelryType.objects.get(name='Bracelet')
    Bracelet = Jewelry.objects.filter(category=Bracelet_category)
    return render(request, 'shop/ring_page.html', {'jewelry_items': Bracelet })


def about1(req):
    return render(req,'shop/about.html')



#-------------------------------------------------------------------------------------------------------------------------------------


def user_home(req):
    if 'user' in req.session:
        products=Jewelry.objects.all()
        return render(req,'user/user_home.html',{'product':products})

def view_pro(req,id):
    log_user=User.objects.get(username=req.session['user'])
    products=Jewelry.objects.get(pk=id)
    try:
        cart=Cart.objects.get(product=products,user=log_user)
    except:
        cart=None
    return render(req,'user/view.html',{'product':products,'cart':cart})

def add_to_cart(req,id):
    products=Jewelry.objects.get(pk=id)
    # print(products)
    user=User.objects.get(username=req.session['user'])
    # print(user)
    data=Cart.objects.create(user=user,product=products)
    data.save()
    return redirect(cart_display)

    
# def cart_display(req):
#     log_user=User.objects.get(username=req.session['user'])
#     data=Cart.objects.filter(user=log_user)
#     return render(req,'user/cart_display.html',{'data':data}) 


def cart_display(req):
    log_user = User.objects.get(username=req.session['user'])
    data = Cart.objects.filter(user=log_user)
    total_price = sum(cart_item.product.price for cart_item in data)
    return render(req, 'user/cart_display.html', {'data': data, 'total_price': total_price})

def delete_cart(req,id):
    data=Cart.objects.get(pk=id)
    data.delete()
    return redirect(cart_display)   


# def buy_pro(req,id):
#     products=Jewelry.objects.get(pk=id)
    # return redirect(address_page, id=id)
    # return render(req,'user/user_dtls.html',{'product':products}) 

def buy_pro(req, id):
    product = Jewelry.objects.get(pk=id)
    return redirect(address_page, id=id)  


def address_page(req, id):
    product = Jewelry.objects.get(pk=id)
    user = User.objects.get(username=req.session['user'])  
    user_address = Address.objects.filter(user=user).order_by('-id').first()

    if req.method == 'POST':
        name = req.POST.get('name')
        address = req.POST.get('address')
        phone_number = req.POST.get('phone_number')
        size = req.POST.get('size', 10) 
        
        if user_address:
            user_address.name = name
            user_address.address = address
            user_address.phone_number = phone_number
            user_address.save()
        else:
            Address.objects.create(user=user, name=name, address=address, phone_number=phone_number)

        req.session['product'] = id
        req.session['size'] = size
        
        return redirect('order_payment')  

    return render(req, 'user/user_dtls.html', {'product': product, 'user_address': user_address})


@login_required
def order_payment(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])  
        product = Jewelry.objects.get(pk=req.session['product'])  
        amount = product.price 
        amount_in_paise = int(amount * 100)  

        print(f"Amount being passed to Razorpay (in paise): {amount_in_paise}")

        razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        razorpay_order = razorpay_client.order.create({
            "amount": amount_in_paise,  
            "currency": "INR",  
            "payment_capture": "1" 
        })

        order = Order.objects.create(
            user=user,
            price=amount, 
            provider_order_id=razorpay_order['id']  
        )
        req.session['order_id'] = order.pk  

        return render(req, "user/payment.html", {
            "callback_url": "http://127.0.0.1:8000/callback/", 
            "razorpay_key": settings.RAZORPAY_KEY_ID, 
            "order": order,  
        })
    return redirect(login)  


@login_required
def pay(req):
    user = User.objects.get(username=req.session['user'])  
    product = Jewelry.objects.get(pk=req.session['product'])

    if not product:
        messages.error(req, "Your cart is empty. Please add a product first.")
        return redirect(cart_display)

    order_id = req.session.get('order_id')
    order = get_object_or_404(Order, pk=order_id) if order_id else None

    if req.method == 'GET':
        user_address = Address.objects.filter(user=user).order_by('-id').first()

        data = Buy.objects.create(
            user=user,
            product=product,
            price=product.price,
            address=user_address,
            order=order
        )
        data.save()

        return redirect(user_view_bookings)

    return render(req, 'user/view_bookings.html')


@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id

        if verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
        else:
            order.status = PaymentStatus.FAILURE

        order.save()
        return redirect(pay)
    else:
        payment_data = json.loads(request.POST.get("error[metadata]", "{}"))
        provider_order_id = payment_data.get("order_id", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.status = PaymentStatus.FAILURE
        order.save()

        return redirect(pay)


def place_order(req, id):
    product = Jewelry.objects.get(pk=id)
    user = req.user
    size = req.POST.get('size', 10)  
    data = Buy.objects.create(
        user=user, 
        product=product, 
        price=product.price,
        quantity=1,  
        address=None,  
        is_confirmed=False,
    )
    data.save()

    return redirect(user_home) 



    


def user_view_bookings(req):
    user=User.objects.get(username=req.session['user'])
    data=Buy.objects.filter(user=user)
    return render(req,'user/view_booking.html',{'data':data})


def about(req):
    return render(req,'user/about.html')



# User Profile Page displaying user details and relevant actions (cart, orders, etc.)
def user_profile(req):
    if 'user' in req.session:
        # Fetch the logged-in user
        log_user = User.objects.get(username=req.session['user'])

        # Get the user's profile details (name, email, etc.)
        user_details = {
            'username': log_user.username,
            'email': log_user.email,
            'full_name': log_user.first_name + " " + log_user.last_name,
            # 'ph_no':log_user.
        }

        # Get the user's active cart items
        cart_items = Cart.objects.filter(user=log_user)

        # Get the user's past orders
        orders = Buy.objects.filter(user=log_user)

        return render(req, 'user/profile.html', {
            'user_details': user_details,
            'cart_items': cart_items,
            'orders': orders
        })
    else:
        return redirect(login)  # Redirect to login page if user is not logged in
# Edit User Profile
def edit_profile(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        
        if req.method == 'POST':
            user.first_name = req.POST.get('first_name')
            user.last_name = req.POST.get('last_name')
            user.email = req.POST.get('email')
            user.save()
            return redirect(user_profile)
        
        return render(req, 'user/edit_profile.html', {'user': user})
    else:
        return redirect(login)

def search(req):
    if req.method == 'POST':
        searched = req.POST.get('searched', '')  
        results = Jewelry.objects.filter(name__icontains=searched) if searched else []
        return render(req, 'user/search.html', {'searched': searched, 'results': results})
    else:
        return render(req, 'user/search.html', {'searched': '', 'results': []})   


#  displaying all Rings
def r_page(request):
    ring_category = JewelryType.objects.get(name='ring') 
    rings = Jewelry.objects.filter(category=ring_category)
    return render(request, 'user/r_page.html', {'jewelry_items': rings})
#  displaying all necklace
def n_page(request):
    necklace_category = JewelryType.objects.get(name='necklace')
    necklaces = Jewelry.objects.filter(category=necklace_category)
    return render(request, 'user/r_page.html', {'jewelry_items': necklaces})
#  displaying all earrings
def e_page(request):
    earrings_category = JewelryType.objects.get(name='earrings')
    earrings = Jewelry.objects.filter(category=earrings_category)
    return render(request, 'user/r_page.html', {'jewelry_items': earrings })

def b_page(request):
    Bracelet_category = JewelryType.objects.get(name='Bracelet')
    Bracelet = Jewelry.objects.filter(category=Bracelet_category)
    return render(request, 'user/r_page.html', {'jewelry_items': Bracelet })


#------------------------------------------------





def checkout(req):
    log_user = User.objects.get(username=req.session['user'])
    
    # Retrieve the cart items for the logged-in user
    cart_items = Cart.objects.filter(user=log_user)
    
    if req.method == 'POST':
        # Handle the purchase (checkout) logic
        # Example: Create a Buy entry for each cart item
        address = Address.objects.get(user=log_user)  # Get the user's address from Address model
        
        # Loop over each cart item and create a Buy object
        for cart_item in cart_items:
            Buy.objects.create(
                user=log_user,
                product=cart_item.product,
                price=cart_item.product.price,
            )
        
        # After purchase, clear the user's cart
        cart_items.delete()
        
        # Redirect to the "Order Confirmation" or any other page
        return redirect(cart_display)

    # If GET request, just show the checkout page
    return render(req, 'user/checkout.html', {'cart_items': cart_items})

# def order_confirmation(req):
#     return render(req, 'user/order_confirmation.html')

