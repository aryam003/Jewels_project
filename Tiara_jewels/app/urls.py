from django.urls import path
from . import views

urlpatterns=[
    path('',views.shop_login),
    path('logout',views.shop_logout),
    path('register',views.register),

#-------------------------------------------------------------------------------------------------------- for shop

    path('shop_home',views.shop_home),
    path('add_product',views.add_product),
    path('edit_pro/<id>/', views.edit_pro),
    path('delete_pro/<id>/',views.delete_pro),
    path('booking',views.bookings),

    path('rings/', views.ring_page, name='ring_page'),         
    path('necklaces/', views.necklace_page, name='necklace_page'), 
    path('earrings/', views.earrings_page, name='earrings_page'), 
    path('Bracelet/', views.Bracelet_page, name='Bracelet_page'), 
    
    # path('jewelry/<int:jewelry_id>/', views.jewelry_detail, name='jewelry_detail'),

#---------------------------------------------------------------------------------------------------------for user

    path('user_home',views.user_home),
    path('view_pro/<id>',views.view_pro),
    path('add_to_cart/<id>',views.add_to_cart),
    path('cart_display',views.cart_display),
    path('delete_cart/<id>',views.delete_cart),
    path('buy_pro/<id>',views.buy_pro),
    path('user_booking',views.user_view_bookings),
    
    path('user_rings/', views.r_page, name='ring_page'),  
    path('user_necklaces/', views.n_page, name='necklace_page'), 
    path('user_earrings/', views.e_page, name='earrings_page'),  
    path('user_Bracelet/', views.b_page, name='Bracelet_page'), 



#-----------------------------------------------------------------------------------------------------------for jewels


]