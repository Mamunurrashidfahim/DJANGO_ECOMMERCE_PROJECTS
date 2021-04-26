from django.contrib import messages
from App_Payment.forms import BillingForm
from App_Payment.models import BillingAddress
from App_Order.models import Cart, Order
from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
#for payment
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Context, Decimal
import socket


@login_required
def cheakout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form =BillingForm(instance=saved_address)
    if request.method =="POST":
        form=BillingForm(request.POST,instance=saved_address)
        if form.is_valid():
            form.save()
            form=BillingForm(instance=saved_address)
            messages.info(request,f"Shipping Address Saved!!!")
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    order_items =order_qs[0].orderitems.all()
    order_total= order_qs[0].get_totals()
    return render(request,'App_Payment/cheakout.html',context={'form':form,'order_items':order_items,'order_total':order_total,'saved_address':saved_address})

@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    if not saved_address.is_fully_filled():
        messages.info(request,f"Please complate Shipping Address!!!")
        return redirect('App_Payment:cheakout')
    
    if not request.user.profile.is_fully_filled():
        messages.info(request,f"Please complate Profile Details!!!")
        return redirect('App_Login:profile')

    store_id = 'mysit6083f1bc9bcf5'
    API_key ='mysit6083f1bc9bcf5@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_key)

    status_url =request.build_absolute_uri(reverse("App_Payment:complate"))
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

    order_qs =Order.objects.filter(user =request.user,ordered=False)
    order_items =order_qs[0].orderitems.all()
    order_items_count =order_qs[0].orderitems.count()
    order_total =order_qs[0].get_totals()
    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed', product_name=order_items, num_of_item=order_items_count, shipping_method='Courier', product_profile='None')

    current_user=request.user
    mypayment.set_customer_info(name=current_user.profile.full_name, 
    email=current_user.email, 
    address1=current_user.profile.address_1, 
    address2=current_user.profile.address_1, 
    city=current_user.profile.city, 
    postcode=current_user.profile.zip_code, 
    country=current_user.profile.country, 
    phone=current_user.profile.phone,)

    mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, 
    address=saved_address.address, 
    city=saved_address.city, 
    postcode=saved_address.zip_code, 
    country=saved_address.country)

    response_data = mypayment.init_payment()
    print(response_data)
    return redirect(response_data['GatewayPageURL'])

@csrf_exempt
def complate(request):
    if request.method =='POST' or request.method =='post':
        payment_data =request.POST
        status = payment_data['status']
        if status =="VALID":
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request,f"Your Payment complate Successfully!!")
            return HttpResponseRedirect(reverse("App_Payment:purchase", kwargs={'val_id':val_id,'tran_id':tran_id,}))
        elif status =="FAILED":
            messages.success(request,f"Your Payment Failed!!Please Try Again!!")
    return render(request,'App_Payment/complate.html',context={'status':status})


@login_required
def purchase(request,val_id,tran_id):
    order_qs =Order.objects.filter(user =request.user,ordered=False)
    order = order_qs[0]
    orderId = tran_id
    order.ordered =True
    order.orderId =orderId
    order.paymentId = val_id
    order.save()
    cart_items=Cart.objects.filter(user =request.user,purchased=False)
    for item in cart_items:
        item.purchased=True
        item.save()
    return HttpResponseRedirect(reverse("App_Shop:home"))

@login_required
def order_view(request):
    try:
        orders=Order.objects.filter(user =request.user,ordered=True)
        context={'orders':orders}
    except:
        messages.warning(request,"You do no Have any active order")
        return redirect('App_Shop:home')
    return render(request,"App_Payment/order.html",context)