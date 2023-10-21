from django.urls import path
from ecommerce import views

urlpatterns = [
    path('',views.index, name="home"),
    path('shop',views.shop, name="shop"),
    path('about',views.about, name="about"),
    path('productdetails/<id>/',views.productdetails, name="productdetails"),
    path('shopping-cart',views.shoppingcart, name="cart"),
    path('checkout',views.checkout,name="checkout"),
    path('update_item/',views.updateItem, name="update_item"),
    path('process_order/',views.processOrder, name="process_order"),
    # path('signup',views.signup,name="signup"),
    # path('signin',views.signin,name="signin"),
    # path('signout',views.signout,name="signout"),
    
]