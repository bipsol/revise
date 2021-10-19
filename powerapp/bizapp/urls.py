from django import urls
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'), #for pulling out all products/items
    path('products/', views.all_products, name='all_products'), #for pulling out all products/items
    path('category/<str:id>/', views.product_category, name='category'), #for pulling out product and category items
    path('detail/<str:id>/', views.product_detail, name='detail'), 
    path('loginform/', views.loginform, name='loginform'), 
    path('logoutform/', views.logoutform, name='logoutform'), 
    path('signupform/', views.signupform, name='signupform'), 
    path('profile/', views.profile, name='profile'), 
    path('update/', views.update, name='update'), 
    path('password/', views.change, name='password'), 
    path('shopcart/', views.shopcart, name='shopcart'), 
    path('cart/', views.cart, name='cart'), 
    path('increase/', views.increase, name='increase'), 
    path('remove/', views.remove, name='remove'), 
    path('checkout/', views.checkout, name='checkout'), 
    path('placeorder/', views.paidorder, name='paidorder'),
    path('completed/', views.completed, name='completed'), 
    ]
