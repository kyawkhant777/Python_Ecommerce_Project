from django.urls import path
from shop_app.views import *

urlpatterns = [
     path('list/', ProductList),
     path('detail/<int:post_id>/', ProductDetail),
     path('cartCreate/<int:product_id>/',CartCreate),
     path('buyproduct/<int:product_id>/',BuyProduct),
     path('cartList/', CartList),
     path('orderList/', orderList),
     path('cartDelete/<int:cart_id>/', CartDelete),
     path('orderDelete/<str:order_name>/', orderDelete),
     path('cartOrderCreate/', CartOrderCreate),
    
]    
