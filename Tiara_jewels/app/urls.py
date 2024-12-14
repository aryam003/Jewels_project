from django.urls import path
from . import views

urlpatterns=[
    path('',views.shop_login),
    path('logout',views.shop_logout),
    path('register',views.register),

#-------------------------------------------------------------------------------------------------------- for shop

    path('shop_home',views.shop_home),
    path('add_product',views.add_product),
    # path('edit_pro/<id>',views.edit_pro),
    path('edit_pro/<id>/', views.edit_pro),
    path('delete_pro/<id>/',views.delete_pro),


    

    path('rings/', views.ring_page, name='ring_page'),         
    path('necklaces/', views.necklace_page, name='necklace_page'), 
    # path('jewelry/<int:jewelry_id>/', views.jewelry_detail, name='jewelry_detail'),

#---------------------------------------------------------------------------------------------------------for user

    path('user_home',views.user_home),

#-----------------------------------------------------------------------------------------------------------for jewels


]