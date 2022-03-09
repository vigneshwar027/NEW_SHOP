from django.urls import path
from item import views



urlpatterns = [    
    path('',views.allprod,name='home'),
    path('checkout/',views.checkout,name='checkout'),
    path('checkout/<slug:updation>/',views.checkout,name='update_address'),
    path('cart/',views.cart,name='cart'),    
    path('search/',views.search,name='search'),    
    path('update_item/',views.update_item,name='update_item'),
    path('<slug:c_slug>/',views.allprod),
    path('product/<slug:p_slug>/',views.proddesc,name='productpage'),
    path('productss/<slug:p_slug>/',views.proddesc,name='oneproduct'),
    
    
]