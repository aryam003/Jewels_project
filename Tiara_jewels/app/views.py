from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from . models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
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
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        send_mail('Eshop registration', 'E_shop account created', settings.EMAIL_HOST_USER, [email])
        try:
            data=User.objects.create_user(first_name=name,username=email,email=email,password=password)
            data.save()
            return redirect(shop_login)
        except:
            messages.warning(req,"user details already exits.")
            return redirect(register)
    else:
        return render(req,'register.html')
    
def public(req):
    return render(req,'public.html')

    

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
    bookings=Buy.objects.all()[::-1]
    user_addresses = Address.objects.filter(user=req.user) 
    return render(req,'shop/booking.html',{'data':bookings,'user_addresses': user_addresses})

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

    
def cart_display(req):
    log_user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=log_user)
    return render(req,'user/cart_display.html',{'data':data}) 

def delete_cart(req,id):
    data=Cart.objects.get(pk=id)
    data.delete()
    return redirect(cart_display)   


def buy_pro(req,id):
    products=Jewelry.objects.get(pk=id)
    # return redirect('address_page')
    return render(req,'user/user_dtls.html',{'product':products}) 


def address_page(req, id):
    product = Jewelry.objects.get(pk=id)
    if req.method == 'POST':
        name = req.POST.get('name')
        address = req.POST.get('address')
        phone_number = req.POST.get('phone_number')
        
        # Save the address
        user_address = Address.objects.create(user=req.user, name=name, address=address, phone_number=phone_number)

        # Convert price to integer if needed
        price = int(product.price)  # Convert the price to an integer before saving
        # Save the purchase
        data = Buy.objects.create(user=req.user, product=product, price=price)

        return redirect('user_home')  # Adjust the redirect URL as necessary

    return render(req, 'user/user_dtls.html', {'product': product})
def place_order(req, id):
    product = Jewelry.objects.get(pk=id)
    user = req.user  # Using req.user directly
    price = int(product.price)  # Convert the price to an integer before saving
    data = Buy.objects.create(user=user, product=product, price=price)
    
    return redirect(user_home)  # Adjust the redirect URL as necessary





def user_view_bookings(req):
    user=User.objects.get(username=req.session['user'])
    data=Buy.objects.filter(user=user)
    return render(req,'user/view_booking.html',{'data':data})

def about(req):
    return render(req,'user/about.html')

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

