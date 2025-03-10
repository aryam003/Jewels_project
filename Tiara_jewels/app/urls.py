from django.urls import path
from . import views

urlpatterns=[
    path('',views.shop_login),
    path('logout',views.shop_logout),
    path('register',views.register),
    # path('',views.public),
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
    path('about1',views.about1),
    
    # path('jewelry/<int:jewelry_id>/', views.jewelry_detail, name='jewelry_detail'),
    path('confirm_order/<order_id>',views.confirm_order, name='confirm_order'),

#---------------------------------------------------------------------------------------------------------for user

    path('user_home',views.user_home),
    path('view_pro/<id>',views.view_pro),
    path('add_to_cart/<id>',views.add_to_cart),
    path('cart_display',views.cart_display),
    path('delete_cart/<id>',views.delete_cart),
    path('buy_pro/<id>',views.buy_pro),
    path('user_booking',views.user_view_bookings),
    path('about',views.about),
    path('search/', views.search, name='search'),
    path('buy/<id>/', views.buy_pro, name='buy_pro'),
    path('address/<id>/', views.address_page, name='address_page'),
    path('place_order/<id>/', views.place_order, name='place_order'),
    
    path('user_rings/', views.r_page, name='ring_page'),  
    path('user_necklaces/', views.n_page, name='necklace_page'), 
    path('user_earrings/', views.e_page, name='earrings_page'),  
    path('user_Bracelet/', views.b_page, name='Bracelet_page'), 

    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('order_payment', views.order_payment, name='order_payment'),
    # path('order_payment', views.order_payment, name='order_payment'),
    path('pay', views.pay, name='pay'),
     
    path('callback/', views.callback, name='callback'),
#-----------------------------------------------------------------------------------------------------------for jewels

    path('checkout/', views.checkout, name='checkout'),
    path('cart/address/', views.cart_address_page, name='cart_address_page'),
    
    # Route to the order payment page (step 2)
    path('order/payment2/', views.order_payment2, name='order_payment2'),
    
    # Route to handle the payment confirmation callback
    path('callback2/', views.callback2, name='callback2'),
    
    # Route to process the payment and finalize the order (final step after payment)
    path('pay2/', views.pay2, name='pay2'),
    

    path('bookings/', views.bookings, name='bookings'),
    path('search_results/', views.search_results, name='search_results'), 
]