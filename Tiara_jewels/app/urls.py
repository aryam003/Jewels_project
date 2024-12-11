from django.urls import path
from . import views

urlpatterns=[
    path('',views.shop_login),
    path('logout',views.shop_logout),
    path('register',views.register),

#-------------------------------------------------------------------------------------------------------- for shop

    path('shop_home',views.shop_home),

#---------------------------------------------------------------------------------------------------------for user

    path('user_home',views.user_home),

#-----------------------------------------------------------------------------------------------------------for jewels

    path('rings/', views.ring_page, name='ring_page'),         # URL for Rings
    path('necklaces/', views.necklace_page, name='necklace_page'), # URL for Necklaces
    # path('jewelry/<int:jewelry_id>/', views.jewelry_detail, name='jewelry_detail'),
]