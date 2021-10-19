import uuid
import random
import string
import requests
import json


from django.contrib.auth.models import User
from django.http.response import HttpResponse
# from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required 

from bizapp.forms import SignupForm, UpdateForm
from .models import Product, Category, Profile, ShopCart,PaidOrder

# from django.http import HttpResponse    #We query on this page



# Create your views here.
def index(request):
    featured = Product.objects.filter(featured=True)    
    latest = Product.objects.filter(new_arrival=True)

    context= {
        'featured':featured,
        'latest': latest 

    }
    return render(request, 'index.html', context)  #we removed context from ds bracket


def categories(request):
    categories = Category.objects.all()

    context = {
        'categories':categories
                
    }
    return render(request, 'categories.html', context)




def all_products(request):
    all_products = Product.objects.all() # To view all these items

    context = {

        'products':all_products
    }
    return render(request, 'all_products.html', context) 




def product_category(request,id):
    single = Product.objects.filter(category_id=id)

    context = {
        'single':single
    }

    return render(request, 'prod_cat.html', context)

    
def product_detail(request,id):
    detail = Product.objects.get(pk=id)
     # note, ds id is to b picked nd made the second paarameter beside word request, and same in the URL
    context = {
        'detail': detail  }

    return render(request, 'detail.html', context)


#Authentication defined
def loginform(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:    #this line up to Invalid username/Password line are only necessary when we couldnt log in as a user to view our work perhaps cos of forgetfulness of the right username or password
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid username/Password')

    return render(request, 'login.html')

def logoutform(request):
    logout(request)
    return redirect('loginform')
  

def signupform(request):
    regform = SignupForm()
    if request.method ==('POST'):
        regform = SignupForm(request.POST)
        if regform.is_valid():
            newreg = regform.save() #this line together withd next 3 lines are necesaary when we include PROFILE
            reg = Profile(user=newreg)
            reg.save()
            login(request, newreg)
            messages.success(request, 'Your signup is successful')
            return redirect('loginform')
        else:
            messages.warning(request, regform.errors)
            return redirect('signupform')

    context = {
        'regform':regform 
    }
    return render(request, 'signup.html', context)

#Authentication defined done



#profile
@login_required(login_url='loginform')
def profile(request):
    profile = Profile.objects.get(user__username=request.user.username)

    context ={
        'profile':profile
    }

    
    return render(request, 'profile.html', context)



# user profile update 
@login_required(login_url='loginform')
def update(request):
    updateform = UpdateForm(instance=request.user.profile) #Instantiating a user request, this is optional
    if request.method ==('POST'):
        updateform = UpdateForm(request.POST, request.FILES, instance=request.user.profile) #Try stop at request.FILES and also see the effect to mark d difference
        if updateform.is_valid(): #
            updateform.save()
            messages.success(request, 'Profile update successful')
            return redirect('profile')
        

    context = {
        'updateform':updateform 
    }
    
    return render(request,'update.html', context)


    #update done


# password change function 
@login_required(login_url='loginform')
def change(request):
    changeform = PasswordChangeForm(request.user)
    if request.method == 'POST':
        changeform = PasswordChangeForm(request.user, request.POST)
        if changeform.is_valid():
            user=changeform.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password change successful!')
            return redirect('profile')
        else:
            messages.error(request, changeform.errors)
            return redirect('password')

    
    context = {
        'changeform':changeform
    }

    return render(request, 'password.html', context)
# password change function 



#shortcart function
@login_required(login_url='loginform')
def shopcart(request):
    if request.method == 'POST':
        quant = int(request.POST['quantity'])
        dpid = request.POST['pid']
        apid = Product.objects.get(pk=dpid)
        cart = ShopCart.objects.filter(paid_order=False, user__username=request.user.username)
        if cart:
            product=ShopCart.objects.filter(user__username=request.user.username, product=apid.id).first()

            #for subsequent/additional orders to d initial cart, d if and else stmt must be in-between the first est 'if and else' stmnt
            if product: # to chk if a product is already in d cart
                product.quantity += quant #to confirm if already in d cart, then increment it
                product.save()
                messages.success(request, 'Product added to cart!')
                return redirect('all_products')

            else:
                newitem = ShopCart()
                newitem.user = request.user
                newitem.product = apid
                newitem.quantity = quant
                newitem.cart_code = cart[0].cart_code #first index of the cart_code created
                newitem.paid_order = False
                newitem.save()               

        else:
            order_number =str(uuid.uuid4())
            newcart = ShopCart()
            newcart.user =request.user
            newcart.product = apid
            newcart.quantity = quant
            newcart.cart_code = order_number
            newcart.paid_order = False
            newcart.save()

        messages.success(request, 'Product added to Cart')
    return redirect('all_products')

        
        
@login_required(login_url='loginform')
def cart(request):    #to display items selected by individual client
    cart = ShopCart.objects.filter(paid_order=False, user__username=request.user.username)

    total =0
    vat = 0
    grand_total = 0

    for item in cart:
        total += item.product.price * item.quantity
    
    vat = 0.075 * total

    grand_total = total + vat

    context = {
        'cart': cart,
        'total': total, 
        'vat': vat,
        'grand_total': grand_total,
        
    }
    return render (request, 'cart.html', context)



# To increase quantity of items
def increase(request):
    increase = request.POST['addup']
    itemid = request.POST['itemid']
    newquantity = ShopCart.objects.get(pk=itemid)
    newquantity.quantity = increase
    newquantity.save()
    messages.success(request,'Item quantity is updated')
    return redirect('cart')


def remove(request):
    remove = request.POST['del']
    ShopCart.objects.filter(pk=remove).delete()
    messages.success(request, 'Item successfully deleted from your cart' )
    return redirect('cart')




def checkout(request):    #to display items selected by individual client
    cart = ShopCart.objects.filter(paid_order=False, user__username=request.user.username)
    profile= Profile.objects.get(user__username=request.user.username)

    total =0
    vat = 0
    grand_total = 0

    for item in cart:
        total += item.product.price * item.quantity
    
    vat = 0.075 * total

    grand_total = total + vat

    context = {
        'cart': cart,        
        'grand_total': grand_total,
        'profile': profile,
        'order_code':cart[0].cart_code 
        
    }
    return render (request, 'checkout.html', context)


    #Integrating to PAYSTACK API
@login_required(login_url='loginform')
def paidorder(request): # Pls chk the word used in d url section...paidorder or placeorder?
    if request.method == 'POST':
        #1 collecting data for paystack use
        api_key='sk_test_c88f79b6d022cf450a44656cb87d5cfb4c52b9ad' # copied from paystack registered page
        curl= 'https://api.paystack.co/transaction/initialize'  #copied from paystack documentation page
        cburl='http://18.222.86.238/completed/'
        total= float(request.POST['gtotal'])*100
        order_num= request.POST['order_no']
        ref_num=''.join(random.choices(string.digits + string.ascii_letters, k=8))
        user = User.objects.get(username= request.user.username)

        headers= {'Authorization': f'Bearer {api_key}'} # It means dbearere /wht gives d authorisation here is the API Key. There's a key beacuse d authorization is a dictionary
        data={'reference':ref_num, 'amount':total, 'order_number':order_num, 'callback_url':cburl, 'email':user.email} #Ds r\are d user's info taking/submitting to PATSTACK for confirmation
        #collection for data for paystack use ends here.
        
        #call now begins to be initiated to paystack
        try:
            r = requests.post(curl, headers=headers, json=data) #This s wen transac is successful, then else block will b exc=ecuted. This is python REQUESTS(to b newly imported) as a POST request, 
        except Exception: #json = javascrip script used for data interchange
            messages.error(request, 'Network busy, refresh you page and try again. Thank you')
            #The exception block will hold brief in case transaction got an error
        else:
            transback = json.loads(r.text) #at ds point, it's clear d transaction is successful
            rd_url= transback['data'] ['authorization_url']
            paid = PaidOrder()
            paid.user = user
            paid.total_paid = total
            paid.cart_code = order_num
            paid.transac_code = ref_num
            paid.paid_order = True
            paid.first_name = user.profile.first_name
            paid.last_name = user.profile.last_name
            paid.phone = user.profile.phone
            paid.address = user.profile.address
            paid.city = user.profile.city
            paid.state = user.profile.state
            paid.save()
        
            #once the items are taken out, the basket shpuld become empty, to ensure this query the ShopCart.
            basket = ShopCart.objects.filter(user__username=request.user.username, paid_order=False)
            for item in basket:
                item.paid_order=True
                item.save()

                #once d items are sold out, take inventory. To ensure this query the ShopCart
                stock = Product.objects.get(pk=item.product.id)
                stock.max_quantity -= item.quantity
                stock.save() #This is simply a stock-taken command

            return redirect(rd_url)
        return redirect('checkout')


def completed(request):
    profile = Profile.objects.get(user__username= request.user.username)

    context = {
        'profile':profile
    }

    return render(request, 'completed.html',context)

