from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from . models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
# from django.shortcuts import render
# from .models import Jewelry, JewelryType
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
        try:
            data=User.objects.create_user(first_name=name,username=email,email=email,password=password)
            data.save()
            return redirect(shop_login)
        except:
            messages.warning(req,"user details already exits.")
            return redirect(register)
    else:
        return render(req,'register.html')
    


    

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
        category_name = req.POST.get('JewelryType')
        file=req.FILES['img'] 
        try:
            category = JewelryType.objects.update(name=category_name)
        except JewelryType.DoesNotExist:
            messages.error(req, "Category does not exist!")
            return redirect('edit_pro')  
        if file:
            Jewelry.objects.filter(pk=id).update(name=name,description=description,material=material,price=price,weight=weight,image=file,category=category)
        else:
            Jewelry.objects.filter(pk=id).update(name=name,description=description,material=material,price=price,weight=weight,category=category_name)
        
        return redirect(ring_page)
    return render(req,'shop/edit_pro.html',{'data':pro})

def delete_pro(req,id):
    data=Jewelry.objects.get(pk=id)
    url=data.img.url
    url=url.split('/')[-1]
    os.remove('media/'+url)
    data.delete()
    return redirect(ring_page)


    




#-------------------------------------------------------------------------------------------------------------------------------------


def user_home(req):
    if 'user' in req.session:
        products=Jewelry.objects.all()
        return render(req,'user/user_home.html',{'product':products})
    






def r_page(request):
    ring_category = JewelryType.objects.get(name='ring') 
    rings = Jewelry.objects.filter(category=ring_category)
    return render(request, 'user/r_page.html', {'jewelry_items': rings})



#------------------------------------------------



#  displaying all Rings
def ring_page(request):
    ring_category = JewelryType.objects.get(name='ring') 
    rings = Jewelry.objects.filter(category=ring_category)
    return render(request, 'shop/ring_page.html', {'jewelry_items': rings})

#  displaying all Necklaces
def necklace_page(request):
    necklace_category = JewelryType.objects.get(name='necklace')
    necklaces = Jewelry.objects.filter(category=necklace_category)
    return render(request, 'shop/necklace_page.html', {'jewelry_items': necklaces})

def earrings_page(request):
    earrings_category = JewelryType.objects.get(name='earrings')
    earrings = Jewelry.objects.filter(category=earrings_category)
    return render(request, 'shop/earrings_page.html', {'jewelry_items': earrings })

# displaying the details of a specific piece of jewelry
# def jewelry_detail(request, jewelry_id):
#     jewelry = Jewelry.objects.get(id=jewelry_id)
#     return render(request, 'jewelry/jewelry_detail.html', {'jewelry': jewelry})

