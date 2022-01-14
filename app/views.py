from os import O_RDWR
from shopkaro.settings import RAZORPAY_API_KEY
import django
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Product,Customer,Cart,OrderPlaced
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import razorpay
client = razorpay.Client(auth=("rzp_test_Kkdle5kEEV51Jj", "xhRhgMgHwr0M699bCYoQZFy0"))
# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
        totalitem=0
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='LW')
        mobiles=Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html',{'topwears':topwears, 'bottomwears':bottomwears,'mobiles':mobiles,'totalitem':totalitem})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        totalitem=0
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request,'app/productdetail.html',{'product':product ,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required
def add_to_cart(request):
    usr=request.user
    product_id=request.GET.get("prod_id")
    # print(product_id)
    product=Product.objects.get(id=product_id)
    Cart(user=usr,product=product).save()
    return redirect('/showcart')

@login_required
def show_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_ammount=70.0
        total_ammount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                temp=(p.quantity *p.product.discounted_price)
                amount+=temp
            total_ammount=shipping_ammount+amount    
            return render(request, 'app/addtocart.html',{'carts':cart,'total_ammount':total_ammount,'amount':amount,'totalitem':totalitem})
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_ammount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            temp=(p.quantity * p.product.discounted_price)
            amount+=temp
        total_amount=shipping_ammount+amount  

        data={
            'quantity':c.quantity ,
            'totalamount':total_amount ,
            'amount':amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            temp=(p.quantity * p.product.discounted_price)
            amount+=temp
        total_amount=shipping_amount+amount  

        data={
            'quantity':c.quantity ,
            'totalamount':total_amount ,
            'amount':amount
        }
        return JsonResponse(data)

def delete_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            temp=(p.quantity * p.product.discounted_price)
            amount+=temp
        total_amount=shipping_amount+amount  

        data={
            
            'totalamount':total_amount ,
            'amount':amount
        }
        return JsonResponse(data)

@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            pincode=form.cleaned_data['pincode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,pincode=pincode)
            reg.save()
            messages.success(request,'Profile Updated Successfully!!!')
            return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

@login_required
def address(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    usr=request.user
    add=Customer.objects.filter(user=usr)
    return render(request, 'app/address.html',{'addresses':add,'active':'btn-primary','totalitem':totalitem})

@login_required
def orders(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    user=request.user
    op=OrderPlaced.objects.filter(user=user)

    return render(request, 'app/orders.html',{'order_placed':op,'totalitem':totalitem})

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    if data==None :
        mobiles=Product.objects.filter(category='M')
    elif data== 'Samsung' or data=='iPhone':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data== 'below50000' :
        mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=50000)
    elif data== 'above50000' :
        mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=50000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

def topwear(request,data=None):
    if data==None :
        topwears=Product.objects.filter(category='TW')
    # print(topwears)
    elif data=='Lee' or data=='NIKE' or data=='Denim' :
        topwears=Product.objects.filter(category='TW').filter(brand=data)
    elif data== 'above499' :
        topwears=Product.objects.filter(category='TW').filter(discounted_price__gt=499)
    elif data== 'below499' :
        topwears=Product.objects.filter(category='TW').filter(discounted_price__lt=499)
    
    return render(request, 'app/topwear.html',{'topwears':topwears})


def bottomwear(request,data=None):
    if data==None :
        bottomwears=Product.objects.filter(category='LW')
    elif data=='Lee'  or data=='Denim' :
        bottomwears=Product.objects.filter(category='LW').filter(brand=data)
    elif data== 'above499' :
        bottomwears=Product.objects.filter(category='LW').filter(discounted_price__gt=499)
    elif data== 'below499' :
        bottomwears=Product.objects.filter(category='LW').filter(discounted_price__lt=499)
    
    return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears})

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! You are registered successfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})

# def login(request):
#  return render(request, 'app/login.html')



@login_required
def checkout(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    user=request.user
    add=Customer.objects.filter(user=user)
    cartitems=Cart.objects.filter(user=user)
    totalcost=Cart.total_cost
    amou=0.0
    shipping_amount=70.0
    total_amount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    for p in cart_product:
        temp=(p.quantity * p.product.discounted_price)
        amou+=temp
    total_amount=shipping_amount+amou

    order_amount = total_amount*100
    order_currency = 'INR'
    # order_receipt = 'order_rcptid_11'
    # notes = {'Shipping address': 'Bommanahalli, Bangalore'}   # OPTIONAL
    # receipt=order_receipt, notes=notes
    payment_order=client.order.create(dict(amount=order_amount, currency=order_currency,payment_capture=1 ))
    payment_order_id=payment_order['id']
    

    return render(request, 'app/checkout.html',{'add':add,'cartitems':cartitems,'totalamount':total_amount,'order_id':payment_order_id,'api_key':RAZORPAY_API_KEY,'amount':total_amount,'totalitem':totalitem})
@login_required
def payment_done(request):
    
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cartitems=Cart.objects.filter(user=user)
    for c in cartitems:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


    